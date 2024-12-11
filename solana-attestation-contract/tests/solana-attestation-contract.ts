import * as anchor from "@coral-xyz/anchor";
import { AnchorError, Program } from "@coral-xyz/anchor";
import { PublicKey, Keypair, SendTransactionError } from "@solana/web3.js";
import { SolanaAttestationContract } from "../target/types/solana_attestation_contract";
import { publicKey } from "@coral-xyz/anchor/dist/cjs/utils";
import { assert, expect } from "chai";

describe("solana-attestation-contract", () => {
  // Configure the client to use the local cluster.
  anchor.setProvider(anchor.AnchorProvider.env());

  const program = anchor.workspace
    .SolanaAttestationContract as Program<SolanaAttestationContract>;

  const payer = Keypair.generate();
  const randomUser = Keypair.generate();
  const zeroArrays32 = new Array(32).fill(0);
  const zeroArrays64 = new Array(64).fill(0);

  it("Airdrop to payer and random user", async () => {
    const tx = await anchor
      .getProvider()
      .connection.requestAirdrop(payer.publicKey, 10000000000);
    await anchor.getProvider().connection.confirmTransaction(tx);

    const tx2 = await anchor
      .getProvider()
      .connection.requestAirdrop(randomUser.publicKey, 10000000000);
    await anchor.getProvider().connection.confirmTransaction(tx2);
  });

  const [authorityData] = PublicKey.findProgramAddressSync(
    [Buffer.from("galadriel")],
    program.programId
  );

  it("Initialize successfully", async () => {
    const tx = await program.methods
      .initialize()
      .accounts({
        signer: payer.publicKey,
      })
      .signers([payer])
      .rpc();
    // Check the authority data
    const data = await program.account.authorityData.fetch(authorityData);
    assert.ok(data.admin.equals(payer.publicKey));
  });

  it("Reinitialize failed", async () => {
    try {
      const tx = await program.methods
        .initialize()
        .accounts({
          signer: randomUser.publicKey,
        })
        .signers([randomUser])
        .rpc();
      assert(false, "should've failed here but didn't ");
    } catch (err) {
      expect(err).to.be.instanceOf(SendTransactionError);
    }
  });

  const [proofRecord] = PublicKey.findProgramAddressSync(
    [Buffer.from("attestation"), Buffer.from(zeroArrays32)],
    program.programId
  );

  it("Add proof successfully", async () => {
    const tx = await program.methods
      .addProof({
        hashedData: zeroArrays32,
        signature: zeroArrays64,
        publicKey: zeroArrays32,
        attestation: zeroArrays32,
      })
      .accountsStrict({
        proofRecord: proofRecord,
        authority: payer.publicKey,
        authorityData: authorityData,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .signers([payer])
      .rpc();

    // Check the proof record
    const data = await program.account.proofRecord.fetch(proofRecord);
    expect(data.hashedData).to.eql(zeroArrays32);
    expect(data.signature).to.eql(zeroArrays64);
    expect(data.publicKey).to.eql(zeroArrays32);
    expect(data.attestation).to.eql(zeroArrays32);
  });

  const newHashedData = new Array(32).fill(1);
  const [newProofData] = PublicKey.findProgramAddressSync(
    [Buffer.from("attestation"), Buffer.from(newHashedData)],
    program.programId
  );

  it("Add proof failed", async () => {
    try {
      const tx = await program.methods
        .addProof({
          hashedData: newHashedData,
          signature: zeroArrays64,
          publicKey: zeroArrays32,
          attestation: zeroArrays32,
        })
        .accountsStrict({
          proofRecord: newProofData,
          authority: randomUser.publicKey,
          authorityData: authorityData,
          systemProgram: anchor.web3.SystemProgram.programId,
        })
        .signers([randomUser])
        .rpc();
      assert(false, "should've failed here but didn't ");
    } catch (err) {
      expect(err).to.be.instanceOf(AnchorError);
      expect((err as AnchorError).error.errorCode.code).to.equal(
        "UnauthorizedSigner"
      );
    }
  });

  it("Add authority successfully", async () => {
    const tx = await program.methods
      .addAuthority()
      .accounts({
        signer: payer.publicKey,
        newAuthority: randomUser.publicKey,
      })
      .signers([payer])
      .rpc();

    // Check the authority data
    const data = await program.account.authorityData.fetch(authorityData);
    assert.ok(data.admin.equals(payer.publicKey));
    assert.ok(data.authorities[0].equals(randomUser.publicKey));
  });

  it("Add authority failed - unauthorized signer", async () => {
    try {
      const tx = await program.methods
        .addAuthority()
        .accounts({
          signer: randomUser.publicKey,
          newAuthority: randomUser.publicKey,
        })
        .signers([randomUser])
        .rpc();
      assert(false, "should've failed here but didn't ");
    } catch (err) {
      expect(err).to.be.instanceOf(AnchorError);
      expect((err as AnchorError).error.errorCode.code).to.equal(
        "UnauthorizedSigner"
      );
    }
  });

  it("Add authority failed - authority already exists", async () => {
    try {
      const tx = await program.methods
        .addAuthority()
        .accounts({
          signer: payer.publicKey,
          newAuthority: randomUser.publicKey,
        })
        .signers([payer])
        .rpc();
      assert(false, "should've failed here but didn't ");
    } catch (err) {
      expect(err).to.be.instanceOf(AnchorError);
      expect((err as AnchorError).error.errorCode.code).to.equal(
        "AuthorityAlreadyExists"
      );
    }
  });

  it("Add authority failed - authority limit reached", async () => {
    // Add 9 more authorities
    for (let i = 0; i < 9; i++) {
      const newAuthority = Keypair.generate();
      const tx = await program.methods
        .addAuthority()
        .accounts({
          signer: payer.publicKey,
          newAuthority: newAuthority.publicKey,
        })
        .signers([payer])
        .rpc();
    }
    try {
      const tx = await program.methods
        .addAuthority()
        .accounts({
          signer: payer.publicKey,
          newAuthority: Keypair.generate().publicKey,
        })
        .signers([payer])
        .rpc();
      assert(false, "should've failed here but didn't ");
    } catch (err) {
      expect(err).to.be.instanceOf(AnchorError);
      expect((err as AnchorError).error.errorCode.code).to.equal(
        "MaxAuthoritiesReached"
      );
    }
  });

  it("Remove authority successfully", async () => {
    const tx = await program.methods
      .removeAuthority()
      .accounts({
        signer: payer.publicKey,
        authority: randomUser.publicKey,
      })
      .signers([payer])
      .rpc();

    // Check the authority data
    const data = await program.account.authorityData.fetch(authorityData);
    assert.ok(data.admin.equals(payer.publicKey));
    assert.ok(!data.authorities.includes(randomUser.publicKey));
    assert.ok(data.authorities.length === 9);
  });

  it("Remove authority failed - unauthorized signer", async () => {
    try {
      const tx = await program.methods
        .removeAuthority()
        .accounts({
          signer: randomUser.publicKey,
          authority: randomUser.publicKey,
        })
        .signers([randomUser])
        .rpc();
      assert(false, "should've failed here but didn't ");
    } catch (err) {
      expect(err).to.be.instanceOf(AnchorError);
      expect((err as AnchorError).error.errorCode.code).to.equal(
        "UnauthorizedSigner"
      );
    }
  });

  it("Remove authority failed - authority not found", async () => {
    try {
      const tx = await program.methods
        .removeAuthority()
        .accounts({
          signer: payer.publicKey,
          authority: randomUser.publicKey,
        })
        .signers([payer])
        .rpc();
      assert(false, "should've failed here but didn't ");
    } catch (err) {
      expect(err).to.be.instanceOf(AnchorError);
      expect((err as AnchorError).error.errorCode.code).to.equal(
        "AuthorityNotFound"
      );
    }
  });

});






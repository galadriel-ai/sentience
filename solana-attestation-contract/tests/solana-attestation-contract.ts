import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { PublicKey, Keypair } from "@solana/web3.js";
import { SolanaAttestationContract } from "../target/types/solana_attestation_contract";
import { publicKey } from "@coral-xyz/anchor/dist/cjs/utils";

describe("solana-attestation-contract", () => {
  // Configure the client to use the local cluster.
  anchor.setProvider(anchor.AnchorProvider.env());

  const program = anchor.workspace
    .SolanaAttestationContract as Program<SolanaAttestationContract>;

  const payer = Keypair.generate();

  it("Airdrop to payer", async () => {
    const tx = await anchor
      .getProvider()
      .connection.requestAirdrop(payer.publicKey, 10000000000);
    await anchor.getProvider().connection.confirmTransaction(tx);
  });

  it("Is initialized!", async () => {
    const tx = await program.methods.initialize().rpc();
    console.log("Your transaction signature", tx);
  });

  const zeroArrays32 = new Array(32).fill(0);
  const zeroArrays64 = new Array(64).fill(0);

  const [authorityData] = PublicKey.findProgramAddressSync(
    [Buffer.from("galadriel")],
    program.programId
  );

  const [attestationRecord] = PublicKey.findProgramAddressSync(
    [Buffer.from("attestation"), Buffer.from(zeroArrays32)],
    program.programId
  );

  it("Add attestation successfully", async () => {
    const tx = await program.methods
      .addAttestation({
        hashedData: zeroArrays32,
        signature: zeroArrays64,
        publicKey: zeroArrays32,
        attestation: zeroArrays32,
      })
      .accountsStrict({
        attestationRecord: attestationRecord,
        authority: payer.publicKey,
        authorityData: authorityData,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .signers([payer])
      .rpc();
    console.log("Your transaction signature", tx);
  });

  const maliciousPayer = Keypair.generate();

  it("Airdrop to malicious payer", async () => {
    const tx = await anchor
      .getProvider()
      .connection.requestAirdrop(maliciousPayer.publicKey, 10000000000);
    await anchor.getProvider().connection.confirmTransaction(tx);
  });

  const newHashedData = new Array(32).fill(1);
  const [newAttestationData] = PublicKey.findProgramAddressSync(
    [Buffer.from("attestation"), Buffer.from(newHashedData)],
    program.programId
  );

  it("Add attestation failed", async () => {
    try {
      const tx = await program.methods
        .addAttestation({
          hashedData: newHashedData,
          signature: zeroArrays64,
          publicKey: zeroArrays32,
          attestation: zeroArrays32,
        })
        .accountsStrict({
          attestationRecord: newAttestationData,
          authority: maliciousPayer.publicKey,
          authorityData: authorityData,
          systemProgram: anchor.web3.SystemProgram.programId,
        })
        .signers([maliciousPayer])
        .rpc();
      console.log("Your transaction signature", tx);
    } catch (err) {
      console.log(err);
    }
  });

  it("Reinitialize failed", async () => {
    try {
      const tx = await program.methods.initialize().rpc();
      console.log("Your transaction signature", tx);
    } catch (err) {
      console.log(err);
    }
  });
});






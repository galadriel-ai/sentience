import asyncio
from borsh_construct import CStruct, U8
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed

# pylint: disable=import-error
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.keypair import Keypair
from solders.signature import Signature
from solders.instruction import Instruction, AccountMeta
from solders.message import Message

from config import settings
from utils import key_manager

PROGRAM_ID = Pubkey.from_string(settings.SOLANA_PROGRAM_ID)
AUTHORITY_DATA_PDA = Pubkey.find_program_address([bytes(b"galadriel")], PROGRAM_ID)[0]


class AttestationProof:
    def __init__(
        self,
        hashed_data: bytes,
        signature: Signature,
        public_key: Pubkey,
        attestation: bytes,
    ):
        self.schema = CStruct(
            "hashed_data" / U8[32],
            "signature" / U8[64],
            "public_key" / U8[32],
            "attestation" / U8[32],
        )
        self.hashed_data = hashed_data
        self.signature = signature
        self.public_key = public_key
        self.attestation = attestation

    def serialize(self):
        return self.schema.build(
            {
                "hashed_data": self.hashed_data,
                "signature": bytes(self.signature),
                "public_key": bytes(self.public_key),
                "attestation": self.attestation,
            }
        )


class ContractClient:
    def __init__(self, url: str, keypair: Keypair = key_manager.get_account()):
        self.client = AsyncClient(url)
        self.keypair = keypair

    async def is_connected(self):
        return await self.client.is_connected()

    async def close(self):
        await self.client.close()

    def get_keypair(self):
        return self.keypair

    async def call_instruction(
        self, signer: list[Keypair], data: bytes, accounts: list[AccountMeta]
    ):
        instruction = Instruction(PROGRAM_ID, data, accounts)
        message = Message([instruction])
        recent_blockhash_response = await self.client.get_latest_blockhash()
        recent_blockhash = recent_blockhash_response.value.blockhash
        transaction = Transaction(signer, message, recent_blockhash)
        return await self.client.send_transaction(
            transaction,
            opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed),
        )

    async def get_recent_blockhash(self):
        await self.client.get_latest_blockhash()

    async def initialize_program(self):
        accounts = [
            AccountMeta(AUTHORITY_DATA_PDA, is_signer=False, is_writable=True),
            AccountMeta(self.keypair.pubkey(), is_signer=True, is_writable=True),
            AccountMeta(SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        ]
        return await self.call_instruction(
            [self.keypair],
            bytes(settings.INSTRUCTION_DISCRIMINATORS["initialize"]),
            accounts,
        )

    async def add_authority(self, authority: Pubkey):
        accounts = [
            AccountMeta(AUTHORITY_DATA_PDA, is_signer=False, is_writable=True),
            AccountMeta(self.keypair.pubkey(), is_signer=True, is_writable=True),
            AccountMeta(authority, is_signer=False, is_writable=False),
        ]
        return await self.call_instruction(
            [self.keypair],
            bytes(settings.INSTRUCTION_DISCRIMINATORS["add_authority"]),
            accounts,
        )

    async def remove_authority(self, authority: Pubkey):
        accounts = [
            AccountMeta(AUTHORITY_DATA_PDA, is_signer=False, is_writable=True),
            AccountMeta(self.keypair.pubkey(), is_signer=True, is_writable=True),
            AccountMeta(authority, is_signer=False, is_writable=False),
        ]
        return await self.call_instruction(
            [self.keypair],
            bytes(settings.INSTRUCTION_DISCRIMINATORS["remove_authority"]),
            accounts,
        )

    async def add_proof(self, proof: AttestationProof):
        if not isinstance(proof.hashed_data, bytes):
            proof.hashed_data = bytes(proof.hashed_data)
        proof_record_pda = Pubkey.find_program_address(
            [b"attestation", proof.hashed_data], PROGRAM_ID
        )[0]
        accounts = [
            AccountMeta(proof_record_pda, is_signer=False, is_writable=True),
            AccountMeta(AUTHORITY_DATA_PDA, is_signer=False, is_writable=True),
            AccountMeta(self.keypair.pubkey(), is_signer=True, is_writable=True),
            AccountMeta(SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        ]
        data = (
            bytes(settings.INSTRUCTION_DISCRIMINATORS["add_proof"]) + proof.serialize()
        )
        return await self.call_instruction([self.keypair], data, accounts)


async def main():
    # Example usage

    client = ContractClient(settings.SOLANA_RPC_URL)
    print(await client.is_connected())
    # response = await client.remove_authority(client.keypair.pubkey())
    # print(response)
    response = await client.add_authority(client.keypair.pubkey())
    print(response)
    array_of_32_bytes = [0] * 32
    array_of_64_bytes = [0] * 64
    response = await client.add_proof(
        AttestationProof(
            array_of_32_bytes, array_of_64_bytes, array_of_32_bytes, array_of_32_bytes
        )
    )
    print(response)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

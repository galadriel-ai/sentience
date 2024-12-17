from utils.solana_client import ContractClient
from service.tee.entities import GetSolanaPublicKeyResponse


async def execute(
    solana_client: ContractClient,
) -> GetSolanaPublicKeyResponse:
    return GetSolanaPublicKeyResponse(
        public_key=str(solana_client.get_keypair().pubkey())
    )

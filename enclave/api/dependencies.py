from utils.solana_client import ContractClient
from config import settings

# pylint: disable=C0103
solana_client = None

# pylint: disable=W0603
def init_globals():
    global solana_client
    solana_client = ContractClient(settings.SOLANA_RPC_URL)

def get_solana_client() -> ContractClient:
    return solana_client

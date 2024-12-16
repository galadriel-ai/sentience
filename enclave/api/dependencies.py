import config.settings as settings
from utils.solana_client import ContractClient

solana_client = None


def init_globals():
    global solana_client
    solana_client = ContractClient(settings.SOLANA_RPC_URL)

def get_solana_client() -> ContractClient:
    return solana_client

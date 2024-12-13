import key_manager

# pylint: disable=import-error
from solders.keypair import Keypair

solana_account: Keypair


# pylint: disable=W0603
def init_globals():
    global solana_account
    solana_account = key_manager.get_account()


def get_solana_account() -> Keypair:
    return solana_account

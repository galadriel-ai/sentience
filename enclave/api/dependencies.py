from typing import Optional

import key_manager
from solders.keypair import Keypair

solana_account = None


def init_globals():
    global solana_account
    solana_account = key_manager.get_account()


def get_solana_account() -> Keypair:
    return solana_account

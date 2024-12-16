import os
from typing import Optional

# pylint: disable=import-error
from solders.keypair import Keypair

from config import settings


def get_account() -> Keypair:
    key = _get_private_key()
    if key:
        print("Loaded existing private key.")
        return Keypair.from_bytes(key)
    print("No private key found, creating a new one.")
    account = Keypair()
    _save_private_key(account)
    return account


def _get_private_key() -> Optional[bytes]:
    if os.path.exists(settings.SOLANA_KEYPAIR_DIR):
        with open(settings.SOLANA_KEYPAIR_DIR, "rb") as file:
            return file.read()
    return None


def _save_private_key(account: Keypair):
    private_key = bytes(account)
    with open(settings.SOLANA_KEYPAIR_DIR, "wb") as file:
        file.write(private_key)

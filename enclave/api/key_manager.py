import os
from typing import Optional

# pylint: disable=import-error
from solders.keypair import Keypair

KEY_FILE = "solana.key"


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
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as file:
            return file.read()
    return None


def _save_private_key(account: Keypair):
    private_key = bytes(account)
    with open(KEY_FILE, "wb") as file:
        file.write(private_key)


def sign_message(account: Keypair, hash_value: bytes) -> bytes:
    """Sign a hash using the account's private key."""
    return account.sign_message(hash_value)

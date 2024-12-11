import hashlib
import os
from typing import Dict

import libnsm
from solders.keypair import Keypair

KEY_FILE = "solana.key"
ROOT_DIR = os.getcwd()


def main():
    account = get_account()
    print(f"Public Key: {account.pubkey()}")
    data = "mock data"
    hash_value = hashlib.sha256(data.encode("utf-8")).digest()
    signature = sign_message(account, hash_value)

    print(f"Hash: {hash_value.hex()}")
    print(f"Signature: {signature}")


def get_account() -> Keypair:
    key = _get_private_key()
    if key:
        print("Loaded existing private key.")
        return Keypair.from_bytes(key)
    else:
        print("No private key found, creating a new one.")
        account = Keypair()
        _save_private_key(account)
        return account


def _get_private_key() -> str:
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


def save_gcp(gcp_creds_json):
    """Save GCP credentials to a JSON file."""
    with open(os.path.join(ROOT_DIR, "sidekik.json"), "w") as file:
        file.write(gcp_creds_json)


if __name__ == "__main__":
    main()

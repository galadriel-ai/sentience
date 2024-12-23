import os
from typing import Optional

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from config import settings


def get_account() -> Ed25519PrivateKey:
    key = _get_private_key()
    if key:
        print("Loaded existing private key.")
        return Ed25519PrivateKey.from_private_bytes(key)
    print("No private key found, creating a new one.")
    private_key = Ed25519PrivateKey.generate()
    _save_private_key(private_key)
    return private_key


def _get_private_key() -> Optional[bytes]:
    if os.path.exists(settings.ENCLAVE_KEYPAIR_DIR):
        with open(settings.ENCLAVE_KEYPAIR_DIR, "rb") as file:
            return file.read()
    return None


def _save_private_key(private_key: Ed25519PrivateKey):
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(settings.ENCLAVE_KEYPAIR_DIR, "wb") as file:
        file.write(private_key_bytes)

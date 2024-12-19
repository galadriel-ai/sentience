from cryptography.hazmat.primitives.asymmetric import ed25519

enclave_keypair: ed25519.Ed25519PrivateKey


# pylint: disable=W0603
def init_globals():
    global enclave_keypair
    enclave_keypair = ed25519.Ed25519PrivateKey.generate()


def get_enclave_keypair() -> ed25519.Ed25519PrivateKey:
    return enclave_keypair

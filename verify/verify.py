import argparse
import base64
from typing import Optional

import attestation_verifier

ATTESTATION_DOC_B64_PATH = "attestation_doc_b64.txt"


def _read_attestation_doc():
    with open(ATTESTATION_DOC_B64_PATH, "r", encoding="utf-8") as file:
        return file.read()


def get_root_pem():
    with open("root.pem", "r", encoding="utf-8") as file:
        return file.read()


def save_public_key(public_key):
    with open("enclave_public_key.txt", "w") as file_out:
        file_out.write(public_key)


def main(
    pcr0: Optional[str],
):
    attestation_doc_b64 = _read_attestation_doc()
    root_cert_pem = get_root_pem()
    attestation_doc = base64.b64decode(attestation_doc_b64)

    try:
        attestation_verifier.verify_attestation_doc(
            attestation_doc=attestation_doc, pcrs=[pcr0], root_cert_pem=root_cert_pem
        )
        print("\nAttestation verification succeeded!")
    except Exception as e:
        # Send error response back to enclave
        print("\nAttestation verification failed!", e)

    b_public_key = attestation_verifier.get_public_key(attestation_doc)
    print("\nbinary public_key:", b_public_key)
    public_key = "0x" + b_public_key.hex()
    print("public_key:", public_key)
    save_public_key(public_key)
    print("\npublic key saved to enclave_public_key.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify pcr0 hash and attestation doc")

    parser.add_argument("--pcr0_hash")
    args = parser.parse_args()
    pcr0_hash = args.pcr0_hash
    if not pcr0_hash:
        raise Exception("No arguments passed, pass --pcr0_hash <hash>")

    main(pcr0_hash)

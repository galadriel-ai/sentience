import argparse
import base64
import json
from typing import Optional
from typing import Tuple

from web3 import Web3

import attestation_verifier

ATTESTATION_DOC_B64_PATH = "attestation_doc_b64.txt"

RPC_URL = "https://devnet.galadriel.com"
web3_client = Web3(Web3.HTTPProvider(RPC_URL))

def _get_oracle_address(tx_hash: str) -> str:
    try:
        tx = web3_client.eth.get_transaction(tx_hash)
        return tx.to
    except:
        raise Exception("Cannot read address from tx hash, make sure correct hash is passed in - tx made by the oracle")


def _read_onchain_attestation(oracle_address: str) -> Tuple[str, str]:
    with open("oracle_abi.json", "r", encoding="utf-8") as f:
        oracle_abi = json.loads(f.read())

    contract = web3_client.eth.contract(
        address=oracle_address, abi=oracle_abi
    )
    try:
        pcr0_hash_owner = contract.functions.latestPcr0HashOwner().call()
        pcr0_hash = contract.functions.pcr0Hashes(pcr0_hash_owner).call()

        attestation_owner = contract.functions.latestAttestationOwner().call()
        attestation = contract.functions.attestations(attestation_owner).call()
    except:
        raise Exception(
            "Cannot read on-chain attestation, make sure correct transaction hash or oracle address is passed")
    return pcr0_hash, attestation


def _read_attestation_doc():
    with open(ATTESTATION_DOC_B64_PATH, "r", encoding="utf-8") as file:
        return file.read()


def get_root_pem():
    with open('root.pem', 'r', encoding="utf-8") as file:
        return file.read()


def save_public_key(public_key):
    with open("enclave_public_key.txt", "w") as file_out:
        file_out.write(public_key)


def main(
    pcr0: Optional[str],
    oracle_address: Optional[str],
    tx_hash: Optional[str],
):
    if tx_hash:
        oracle_address = _get_oracle_address(tx_hash)
        print(f"Got oracle address: {oracle_address} from tx hash!")
    if oracle_address:
        pcr0, attestation_doc_b64 = _read_onchain_attestation(oracle_address)
        print(f"Got pcr0 hash and attestation doc from oracle contract!")
    else:
        attestation_doc_b64 = _read_attestation_doc()

    root_cert_pem = get_root_pem()

    attestation_doc = base64.b64decode(attestation_doc_b64)

    try:
        attestation_verifier.verify_attestation_doc(
            attestation_doc=attestation_doc,
            pcrs=[pcr0],
            root_cert_pem=root_cert_pem
        )
        print("Attestation verification succeeded!")
    except Exception as e:
        # Send error response back to enclave
        print("Attestation verification failed!")

    b_public_key = attestation_verifier.get_public_key(attestation_doc)
    print("\nbinary public_key:", b_public_key)
    public_key = "0x" + b_public_key.hex()
    print("public_key:", public_key)
    save_public_key(public_key)
    print("\npublic key saved to enclave_public_key.txt")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Verify pcr0 hash and attestation doc"
    )

    parser.add_argument("--pcr0_hash")
    parser.add_argument("--oracle_address")
    parser.add_argument("--tx_hash")
    args = parser.parse_args()
    pcr0_hash = args.pcr0_hash
    oracle_address = args.oracle_address
    tx_hash = args.tx_hash
    if not pcr0_hash and not oracle_address and not tx_hash:
        raise Exception(
            "No arguments passed, pass either --pcr0_hash <hash>, --oracle_address <oracle contract address> or --tx_hash <tx made by oracle>")

    main(pcr0_hash, oracle_address, tx_hash)

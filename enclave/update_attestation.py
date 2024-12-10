import asyncio
import json
import base64
import time

from eth_account.signers.local import LocalAccount
from web3 import AsyncWeb3

import key_manager
import settings

SLEEP = 5

web3_client = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(settings.WEB3_RPC_URL))

with open(settings.ORACLE_ABI_PATH, "r", encoding="utf-8") as f:
    oracle_abi = json.loads(f.read())["abi"]


async def main():
    while True:
        account: LocalAccount = key_manager.get_account()
        print("Account:", account.address)
        attestation_doc_b64 = get_attestation_doc()
        await send_attestation(account, attestation_doc_b64)
        print(f"Sleeping for {SLEEP} seconds until next update")
        time.sleep(SLEEP)


def get_attestation_doc():
    try:
        from NsmUtil import NSMUtil
        nsm_util = NSMUtil()
        attestation_doc = nsm_util.get_attestation_doc()
        attestation_doc_b64 = base64.b64encode(attestation_doc).decode()
        return attestation_doc_b64
    except Exception as exc:
        print("Error in getting attestation:", exc)
        return "MockAttestation"


async def send_attestation(account: LocalAccount, attestation_doc_b64: str):
    nonce = await web3_client.eth.get_transaction_count(account.address)
    tx_data = {
        "from": account.address,
        "nonce": nonce,
        # TODO: pick gas amount in a better way
        # "gas": 1000000,
        "maxFeePerGas": web3_client.to_wei("2", "gwei"),
        "maxPriorityFeePerGas": web3_client.to_wei("1", "gwei"),
    }
    if chain_id := settings.CHAIN_ID:
        tx_data["chainId"] = int(chain_id)

    oracle_contract = web3_client.eth.contract(
        address=settings.ORACLE_ADDRESS, abi=oracle_abi
    )
    tx = await oracle_contract.functions.addAttestation(
        attestation_doc_b64,
    ).build_transaction(tx_data)
    print("\ntx_data:", tx_data)
    signed_tx = web3_client.eth.account.sign_transaction(
        tx, private_key=account.key
    )
    print("\nsigned_tx")
    tx_hash = await web3_client.eth.send_raw_transaction(
        signed_tx.rawTransaction
    )
    print("\ntx_hash:", tx_hash)
    tx_receipt = await web3_client.eth.wait_for_transaction_receipt(tx_hash)
    print("\ntx_receipt:", tx_receipt)


if __name__ == '__main__':
    asyncio.run(main())

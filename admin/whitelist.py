import asyncio
import json
import argparse

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import AsyncWeb3

import settings

web3_client = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(settings.WEB3_RPC_URL))

with open(settings.ORACLE_ABI_PATH, "r", encoding="utf-8") as f:
    oracle_abi = json.loads(f.read())["abi"]


async def main(whitelist_address: str):
    account: LocalAccount = Account.from_key(settings.PRIVATE_KEY)
    print("Account:", account.address)
    await whitelist(account, whitelist_address)


async def whitelist(signing_account: LocalAccount, whitelist_address: str):
    nonce = await web3_client.eth.get_transaction_count(signing_account.address)
    tx_data = {
        "from": signing_account.address,
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
    tx = await oracle_contract.functions.updateWhitelist(
        whitelist_address,
        True,
    ).build_transaction(tx_data)

    print("\ntx_data:", tx_data)
    signed_tx = web3_client.eth.account.sign_transaction(
        tx, private_key=signing_account.key
    )
    print("\nsigned_tx")
    tx_hash = await web3_client.eth.send_raw_transaction(
        signed_tx.rawTransaction
    )
    print("\ntx_hash:", tx_hash)
    tx_receipt = await web3_client.eth.wait_for_transaction_receipt(tx_hash)
    print("\ntx_receipt:", tx_receipt)


async def send_attestation(account: LocalAccount, attestation: str):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--whitelist_address", type=str, required=True)
    args = parser.parse_args()
    asyncio.run(main(args.whitelist_address))

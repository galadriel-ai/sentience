import asyncio
import json
import os
from api.utils import solana_client, key_manager
from api.config import settings

# pylint: disable=import-error
from solders.keypair import Keypair

KEYPAIR_DIR = "~/.config/solana/id.json"


async def main():
    # Create a ContractClient object
    keypair = None
    with open(os.path.expanduser(KEYPAIR_DIR), "r", encoding="utf-8") as file:
        seed = json.load(file)
        keypair = Keypair.from_bytes(seed)
    if not keypair:
        print("No key file found, exit...")
        return
    client = solana_client.ContractClient(settings.SOLANA_RPC_URL, keypair)
    # Call the is_connected method of the client object
    is_connected = await client.is_connected()
    # Print the result
    print(is_connected)
    # Call the add_authority method of the client object
    enclave_pubkey = key_manager.get_account().pubkey()
    response = await client.add_authority(enclave_pubkey)
    print(response)
    # Call the close method of the client object
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

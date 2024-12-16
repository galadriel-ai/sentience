import asyncio
import json
import os
import api.utils.solana_client as solana_client
import api.utils.key_manager as key_manager
import api.config.settings as settings
from solders.keypair import Keypair

KEYPAIR_DIR = "~/.config/solana/id.json"

async def main():
    # Create a ContractClient object
    keypair = None
    with open(os.path.expanduser(KEYPAIR_DIR), "r") as file:
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

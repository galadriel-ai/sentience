from typing import Optional

import argparse
import asyncio
import json
import os
import sys

# pylint: disable=import-error
from solders.keypair import Keypair
from solders.pubkey import Pubkey

script_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.join(script_dir, "api")
sys.path.append(api_dir)
# pylint: disable=C0413
from utils import solana_client
from config import settings

KEYPAIR_DIR = "~/.config/solana/id.json"


async def main(arg_add: Optional[str], arg_remove: Optional[str]):
    # Create a ContractClient object
    keypair = None
    with open(os.path.expanduser(KEYPAIR_DIR), "r", encoding="utf-8") as file:
        seed = json.load(file)
        keypair = Keypair.from_bytes(seed)
    if not keypair:
        print("No key file found, exit...")
        return
    print(f"Loaded keypair: {keypair.pubkey()}")
    client = solana_client.ContractClient(settings.SOLANA_RPC_URL, keypair)
    # Call the is_connected method of the client object
    is_connected = await client.is_connected()
    # Print the result
    if not is_connected:
        print("Failed to connect to Solana RPC")
        return

    if arg_add:
        # Call the add_authority method of the client object
        print(f"Adding authority: {arg_add}")
        response = await client.add_authority(Pubkey.from_string(arg_add))
        print(response)
    elif arg_remove:
        # Call the remove_authority method of the client object
        print(f"Removing authority: {arg_remove}")
        response = await client.remove_authority(Pubkey.from_string(arg_remove))
        print(response)

    # Call the close method of the client object
    await client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add or remove authority to/from Solana contract"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--add", help="Public key to add as authority")
    group.add_argument("-r", "--remove", help="Public key to remove as authority")
    args = parser.parse_args()
    asyncio.run(main(args.add, args.remove))

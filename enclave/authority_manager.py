import argparse
import asyncio
import json
import os
import sys

# pylint: disable=import-error
from solders.keypair import Keypair
from solders.pubkey import Pubkey

# Add the absolute path of the 'api' directory to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
api_dir = os.path.join(script_dir, "api")
sys.path.append(api_dir)

from utils import solana_client, key_manager
from config import settings

KEYPAIR_DIR = "~/.config/solana/id.json"


async def main(args: argparse.Namespace):
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

    if args.add:
        # Call the add_authority method of the client object
        print(f"Adding authority: {args.add}")
        response = await client.add_authority(Pubkey.from_string(args.add))
        print(response)
    elif args.remove:
        # Call the remove_authority method of the client object
        print(f"Removing authority: {args.remove}")
        response = await client.remove_authority(Pubkey.from_string(args.remove))
        print(response)

    # Call the close method of the client object
    await client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add or remove authority to/from Solana contract")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--add", help="Public key to add as authority")
    group.add_argument("-r", "--remove", help="Public key to remove as authority")
    args = parser.parse_args()
    asyncio.run(main(args))

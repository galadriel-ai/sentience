import json
import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path("..") / ".env"
load_dotenv(dotenv_path=env_path)

# TODO use mainnet url for production
SOLANA_RPC_URL = os.getenv("SOLANA_DEVNET_URL", "https://api.devnet.solana.com")

SOLANA_PROGRAM_ID = os.getenv("SOLANA_PROGRAM_ID", "HCkvLKhWQ8TTRdoSry29epRZnAoEDhP9CjmDS8jLtY9")
SOLANA_KEYPAIR_DIR = os.getenv("SOLANA_KEYPAIR_DIR", "solana.id.json")
INSTRUCTION_DISCRIMINATORS = {
    "add_authority": [229, 9, 106, 73, 91, 213, 109, 183],
    "remove_authority": [242, 104, 208, 132, 190, 250, 74, 216],
    "add_proof": [107, 208, 160, 164, 154, 140, 136, 102],
    "initialize": [175, 175, 109, 31, 13, 152, 155, 237],
}

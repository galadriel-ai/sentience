import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path("..") / ".env"
load_dotenv(dotenv_path=env_path)

ENCLAVE_KEYPAIR_DIR = os.getenv("SOLANA_KEYPAIR_DIR", "solana.key")

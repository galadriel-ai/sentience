from typing import Dict

from dotenv import load_dotenv
import os

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

CHAIN_ID = os.getenv("CHAIN_ID", "")
WEB3_RPC_URL = os.getenv("WEB3_RPC_URL", "")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
ORACLE_ADDRESS = os.getenv("ORACLE_ADDRESS", "")
ORACLE_ABI_PATH = os.getenv("ORACLE_ABI_PATH", "")

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "galadriel-assets")
E2B_API_KEY = os.getenv("E2B_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

PINATA_API_JWT = os.getenv("PINATA_API_JWT", "")
PINATA_GATEWAY_TOKEN = os.getenv("PINATA_GATEWAY_TOKEN", "")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

def get_dot_env() -> Dict:
    return {
        "ENVIRONMENT": "production",
        "OPEN_AI_API_KEY": OPEN_AI_API_KEY,
        "SERPER_API_KEY": SERPER_API_KEY,
        "CHAIN_ID": CHAIN_ID,
        "WEB3_RPC_URL": WEB3_RPC_URL,
        "ORACLE_ADDRESS": ORACLE_ADDRESS,
        "ORACLE_ABI_PATH": "/app/oracles/abi/ChatOracle.json",
        "GCS_BUCKET_NAME": GCS_BUCKET_NAME,
        "E2B_API_KEY": E2B_API_KEY,
        "GROQ_API_KEY": GROQ_API_KEY,
        "PINATA_API_JWT": PINATA_API_JWT,
        "PINATA_GATEWAY_TOKEN": PINATA_GATEWAY_TOKEN,
        "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY,
    }

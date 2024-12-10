from dotenv import load_dotenv
import os

load_dotenv()

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
CHAIN_ID = 696969
WEB3_RPC_URL = os.getenv("WEB3_RPC_URL", "https://devnet.galadriel.com/")
ORACLE_ADDRESS = os.getenv("ORACLE_ADDRESS")
ORACLE_ABI_PATH = os.getenv("ORACLE_ABI_PATH", "oracles/ChatOracle.json")

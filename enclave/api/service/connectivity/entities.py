from pydantic import BaseModel
from pydantic import Field


class CheckConnectivityResponse(BaseModel):
    openai: bool = Field(description="OpenAI connectivity status")
    solana_mainnet: bool = Field(description="Solana Mainnet connectivity status")
    solana_devnet: bool = Field(description="Solana Devnet connectivity status")

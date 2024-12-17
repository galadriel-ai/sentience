from pydantic import BaseModel
from pydantic import Field


class GetSolanaPublicKeyResponse(BaseModel):
    public_key: str = Field(description="Solana public key")

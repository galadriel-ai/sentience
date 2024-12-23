from pydantic import BaseModel
from pydantic import Field


class CheckConnectivityResponse(BaseModel):
    openai: bool = Field(description="OpenAI connectivity status")

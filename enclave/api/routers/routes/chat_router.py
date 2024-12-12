from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import Request

import dependencies
from service.completions.entities import ChatCompletion
from service.completions.entities import ChatCompletionRequest
from service.completions import chat_completions_service

TAG = "Chat"
router = APIRouter(prefix="/chat")
router.tags = [TAG]


@router.post(
    "/completions",
    summary="Creates a model response for the given chat conversation.",
    description="Given a list of messages comprising a conversation, the model will return a response.",
    response_description="Returns a chat completion object",
    response_model=ChatCompletion,
)
async def completions(
    api_request: Request,
    request: ChatCompletionRequest,
    solana_account=Depends(dependencies.get_solana_account),
    authorization: str = Header(...),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Invalid Authorization header format"
        )

    api_key = authorization.split(" ", 1)[1]
    return await chat_completions_service.execute(
        api_key, request, api_request, solana_account
    )

import base64
import hashlib
import json
from typing import Optional

import openai
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import Response

import dependencies
from nsm_util import NSMUtil
from service.completions.entities import ChatCompletion
from service.completions.entities import ChatCompletionRequest


nsm_util = NSMUtil()


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
    request: ChatCompletionRequest,
    response: Response,
    solana_account=Depends(dependencies.get_solana_account),
    authorization: str = Header(...),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Invalid Authorization header format"
        )

    api_key = authorization.split(" ", 1)[1]
    client = openai.AsyncOpenAI(api_key=api_key)

    try:
        params = await request.to_openai_chat_completion()
        openai_response = await client.chat.completions.create(**params)  # type: ignore
        response_dict = (
            openai_response
            if isinstance(openai_response, dict)
            else openai_response.dict()
        )

        # make hash deterministic
        combined_str = f"{json.dumps(params, sort_keys=True)}{json.dumps(response_dict, sort_keys=True)}"
        hash_value = hashlib.sha256(combined_str.encode("utf-8")).digest()
        response_dict["hash"] = hash_value.hex()
        response_dict["signature"] = str(solana_account.sign_message(hash_value))
        attestation_doc = nsm_util.get_attestation_doc(bytes(solana_account.pubkey()))
        attestation_doc_b64 = base64.b64encode(attestation_doc).decode()
        response_dict["attestation"] = attestation_doc_b64
        return response_dict
    except openai.APIError as e:
        raise HTTPException(
            status_code=503, detail=f"Error communicating with OpenAI: {str(e)}"
        )

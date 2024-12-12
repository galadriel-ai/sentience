import base64
import hashlib
import json

import openai
from fastapi import HTTPException
from fastapi import Request
from solders.keypair import Keypair

from nsm_util import NSMUtil
from service.completions.entities import ChatCompletion
from service.completions.entities import ChatCompletionRequest

nsm_util = NSMUtil()


async def execute(
    api_key: str,
    request: ChatCompletionRequest,
    api_request: Request,
    solana_account: Keypair,
) -> ChatCompletion:
    client = openai.AsyncOpenAI(api_key=api_key)

    try:
        params = await request.to_openai_chat_completion()
        openai_response = await client.chat.completions.create(**params)  # type: ignore
        hash_value = await _hash_request_and_response(api_request, openai_response)

        response = ChatCompletion(
            **openai_response.dict(),
            hash=hash_value.hex(),
            signature=str(solana_account.sign_message(hash_value)),
            attestation=_generate_attestation_document(solana_account),
        )
        return response
    except openai.APIError as e:
        raise HTTPException(
            status_code=503, detail=f"Error communicating with OpenAI: {str(e)}"
        )


async def _hash_request_and_response(
    request: Request, response: ChatCompletion
) -> bytes:
    request_body = await request.json()
    combined_str = f"{json.dumps(request_body, sort_keys=True)}{json.dumps(response.dict(), sort_keys=True)}"
    return hashlib.sha256(combined_str.encode("utf-8")).digest()


def _generate_attestation_document(solana_account: Keypair) -> str:
    nsm_util
    attestation_doc = nsm_util.get_attestation_doc(bytes(solana_account.pubkey()))
    return base64.b64encode(attestation_doc).decode()

import base64
import hashlib
import json

import openai
from openai.types.chat.chat_completion import ChatCompletion as OpenAIChatCompletion
from fastapi import HTTPException
from fastapi import Request

from nsm_util import NSMUtil
from service.completions.entities import ChatCompletion
from service.completions.entities import ChatCompletionRequest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

nsm_util = NSMUtil()


async def execute(
    api_key: str,
    request: ChatCompletionRequest,
    api_request: Request,
    enclave_keypair: Ed25519PrivateKey,
) -> ChatCompletion:
    client = openai.AsyncOpenAI(api_key=api_key)

    try:
        params = await request.to_openai_chat_completion()
        openai_response = await client.chat.completions.create(**params)  # type: ignore
        hash_value = await _hash_request_and_response(api_request, openai_response)

        signature = enclave_keypair.sign(hash_value)

        enclave_pubkey = enclave_keypair.public_key().public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
        )

        attestation_doc = _generate_attestation_document(enclave_pubkey)

        response = ChatCompletion(
            **openai_response.dict(),
            hash=hash_value.hex(),
            public_key=enclave_pubkey.hex(),
            signature=signature.hex(),
            attestation=attestation_doc,
        )
        return response
    except openai.APIError as e:
        raise HTTPException(status_code=503, detail=f"Error communicating with OpenAI: {str(e)}")


async def _hash_request_and_response(
    request: Request, response: OpenAIChatCompletion
) -> bytes:
    request_body = await request.json()
    combined_str = f"{json.dumps(request_body, sort_keys=True)}{json.dumps(response.dict(), sort_keys=True)}"
    return hashlib.sha256(combined_str.encode("utf-8")).digest()


def _generate_attestation_document(enclave_pubkey: Ed25519PublicKey) -> str:
    attestation_doc = nsm_util.get_attestation_doc(enclave_pubkey)
    return base64.b64encode(attestation_doc).decode()

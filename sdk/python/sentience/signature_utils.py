import binascii
from typing import Optional
from typing import Union

import nacl.signing
import nacl.exceptions

from openai.types.chat import ChatCompletion

from sentience.history import GaladrielChatHistory


def verify_signature(completion: Union[ChatCompletion, GaladrielChatHistory]) -> bool:
    if not _is_input_with_all_fields(completion):
        return False

    public_key_bytes = _get_public_key(completion)
    if not public_key_bytes:
        return False

    # Decode the hash (message) and signature from hex
    message_bytes = binascii.unhexlify(completion.hash)
    signature_bytes = binascii.unhexlify(completion.signature)

    # Create a VerifyKey object from the public key bytes
    verify_key = nacl.signing.VerifyKey(public_key_bytes)

    try:
        # If verify() does not raise an exception, the signature is valid.
        verify_key.verify(message_bytes, signature_bytes)
        return True
    except nacl.exceptions.BadSignatureError:
        return False


def _is_input_with_all_fields(completion: ChatCompletion) -> bool:
    try:
        return completion.public_key and completion.hash and completion.signature
    except AttributeError:
        return False


def _get_public_key(completion: ChatCompletion) -> Optional[bin]:
    try:
        return binascii.unhexlify(completion.public_key)
    except:
        return None

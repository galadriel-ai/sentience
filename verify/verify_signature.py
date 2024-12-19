import binascii
import base58
import nacl.signing
import nacl.exceptions

# Given values
hash_hex = "ce855e4a2c6fc713c3c5b629ada24cf119f8ed37cce719c8b51ef1841206b020"
signature_hex = "afb7252df102fd4fd15e2791fe5170dad4b9d775eb5ac31cc6a9c040d62bb673e0e481128f5c4e0a1f8c031298278e57710525222a4f8029270f4e10017c6901"
public_key_b58 = "Dp2k554Ebsij5RjuhjsZujVW2bJnQzfb43VYZSQ4NZo1"

# Decode the public key from base58 into raw bytes
public_key_bytes = base58.b58decode(public_key_b58)

# Decode the hash (message) and signature from hex
message_bytes = binascii.unhexlify(hash_hex)
signature_bytes = binascii.unhexlify(signature_hex)

# Create a VerifyKey object from the public key bytes
verify_key = nacl.signing.VerifyKey(public_key_bytes)

try:
    # If verify() does not raise an exception, the signature is valid.
    verify_key.verify(message_bytes, signature_bytes)
    print("Signature is valid!")
except nacl.exceptions.BadSignatureError:
    print("Signature is invalid!")
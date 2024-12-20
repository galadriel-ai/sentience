# pip install pynacl
# python verify.py
import binascii
import nacl.signing
import nacl.exceptions

# Given values
# TODO: change to your values
hash = "c847e98b1abf528f988c0253840616405a014ef2494e7a1b6c8d35e90413dd0a"
signature = "68603b802f1e293dbf21bb1004bd08bca272fc70b6d00556f2a06b35949319533ad527c614c063836601aa00c8ca960dc600cad990df1ff8ff18079a09561d07"
public_key = "835cc0e84c2a5190561d7c2eaf10eb2597cbe7a71541084c5edea32b60bc5e68"

public_key_bytes = binascii.unhexlify(public_key)
# Decode the public key from base58 into raw bytes

# Decode the hash (message) and signature from hex
message_bytes = binascii.unhexlify(hash)
signature_bytes = binascii.unhexlify(signature)

# Create a VerifyKey object from the public key bytes
verify_key = nacl.signing.VerifyKey(public_key_bytes)

try:
    # If verify() does not raise an exception, the signature is valid.
    verify_key.verify(message_bytes, signature_bytes)
    print("Signature is valid!")
except nacl.exceptions.BadSignatureError:
    print("Signature is invalid!")

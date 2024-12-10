import argparse

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

import base64

parser = argparse.ArgumentParser(description="Verify signature")
parser.add_argument(
    "--message",
    type=str,
    required=True,
    help="message"
)
parser.add_argument(
    "--signature",
    type=str,
    required=True,
    help="signature"
)
parser.add_argument(
    "--public_key_path",
    type=str,
    default="enclave_public_key.pem",
    help="public key path"
)

args = parser.parse_args()

signature = base64.b64decode(args.signature)

public_key = RSA.import_key(open(args.public_key_path).read())
try:
    hash_obj = SHA256.new(str.encode(args.message))
    pkcs1_15.new(public_key).verify(hash_obj, signature)
    print("The signature is valid.")
except (ValueError, TypeError):
    print("The signature is not valid.")

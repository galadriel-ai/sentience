from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

import base64

# Load or generate your RSA private key
private_key = RSA.generate(2048)
private_key_der = private_key.export_key(format='DER')
print("Private Key:", private_key_der.hex())

# Your message to sign
message = str.encode("Hello world")
hash_obj = SHA256.new(message)

# Sign the message
signature = pkcs1_15.new(private_key).sign(hash_obj)
signature_b64 = base64.b64encode(signature).decode()
print("\nsignature_b64:", signature_b64)

# Export the private key to PEM format
private_key_pem = private_key.export_key()
with open("private_key.pem", "wb") as file_out:
    file_out.write(private_key_pem)

# Optionally, export the public key to PEM format as well
public_key = private_key.publickey()
public_key_pem = public_key.export_key()
with open("public_key.pem", "wb") as file_out:
    file_out.write(public_key_pem)


# To verify, load the public key, and check the signature
public_key = RSA.import_key(open("public_key.pem").read())
try:
    hash_obj2 = SHA256.new(b"Hello world")
    print("hash_obj2:", hash_obj2)
    pkcs1_15.new(public_key).verify(hash_obj2, signature)
    print("The signature is valid.")
except (ValueError, TypeError):
    print("The signature is not valid.")

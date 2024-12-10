from ecdsa import SigningKey, SECP256k1
import hashlib

# Generate a new private key
private_key = SigningKey.generate(curve=SECP256k1)

# Get the corresponding public key
public_key = private_key.get_verifying_key()

# Convert both keys to strings for display or storage
private_key_hex = private_key.to_string().hex()
public_key_hex = public_key.to_string().hex()

print("Private Key:", private_key_hex)
print("Public Key:", public_key_hex)

# === Sign message === #

message = b"Hello, this is a test message!"

# Step 3: Sign the message
# It's a good practice to hash the message first
hashed_message = hashlib.sha256(message).digest()
signature = private_key.sign(hashed_message)

print("\nSignature:", signature.hex())

# == Validate message === #
try:
    # Note: Ensure to hash the message similarly as done during signing
    verify_result = public_key.verify(signature, hashed_message)
    print("\nVerification result:", verify_result)  # True if successful
except Exception as e:
    print("\nVerification failed:", e)

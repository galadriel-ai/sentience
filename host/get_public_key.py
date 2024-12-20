import urllib.request
import urllib.error
import json

HOST = "127.0.0.1"
PORT = "5000"


def get_public_key():
    url = f"http://{HOST}:{PORT}/v1/tee/public-key"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data["public_key"]
    except urllib.error.URLError:
        return "Error: Could not connect to the enclave, make sure both TEE and the proxy are running"


public_key = get_public_key()
print(f"Enclave public key: {public_key}")

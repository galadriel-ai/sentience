import httpx

HOST = "127.0.0.1"
PORT = "5000"


def get_public_key():
    try:
        response = httpx.get(f"http://{HOST}:{PORT}/v1/tee/public-key")
        return response.json()["public_key"]
    except httpx.ConnectError:
        return "Error: Could not connect to the enclave, make sure both TEE and the proxy is running"


public_key = get_public_key()
print(public_key)

import urllib.request
import urllib.error
import json

HOST = "127.0.0.1"
PORT = "5000"


def check_connectivity():
    url = f"http://{HOST}:{PORT}/v1/connectivity"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except urllib.error.URLError:
        return "Error: Could not connect to the enclave, make sure both TEE and the proxy are running"


connectivity = check_connectivity()
print(f"Enclave connectivity: {connectivity}")

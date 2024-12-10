import socket
import json
import subprocess
import time
from typing import Dict
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse


app = FastAPI()

fetch_metrics_failures_count = 0


def _action_ps(s):
    s.send(
        str.encode(
            json.dumps(
                {
                    "action": "ps",
                }
            )
        )
    )
    response = s.recv(65536)
    return json.loads(response.decode())


def _get_enclave_metrics() -> Dict:
    try:
        cid = _get_cid()
        if not cid:
            return None
        # Create a vsock socket object
        s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        s.settimeout(100.0)
        # The port should match the server running in enclave
        port = 5000
        # Connect to the server
        s.connect((cid, port))
        metrics = _action_ps(s)
        s.close()
        return metrics
    except Exception as exc:
        print("Failed to connect, exc:", exc, flush=True)
        return None


def _format_metrics(data: dict):
    global fetch_metrics_failures_count
    metrics = ""
    enclave_running = 0
    # CPU metrics
    if data:
        enclave_running = 1
        for i in range(data["cpu_count"]):
            metrics += f"# HELP enclave_cpu_usage_core{i} CPU usage percentage for core {i}\n"
            metrics += f"# TYPE enclave_cpu_usage_core{i} gauge\n"
            metrics += f"enclave_cpu_usage_core{i} {data['cpu_usage'][str(i)]}\n"
        # Memory metrics
        metrics += f"# HELP enclave_memory_used Memory used in bytes\n"
        metrics += f"# TYPE enclave_memory_used gauge\n"
        metrics += f"enclave_memory_used {data['ram_used']}\n"
        metrics += f"# HELP enclave_memory_total Total memory in bytes\n"
        metrics += f"# TYPE enclave_memory_total gauge\n"
        metrics += f"enclave_memory_total {data['ram_total']}\n"

        # Disk metrics
        metrics += f"# HELP enclave_disk_used Disk used in bytes\n"
        metrics += f"# TYPE enclave_disk_used gauge\n"
        metrics += f"enclave_disk_used {data['disk_used']}\n"
        metrics += f"# HELP enclave_disk_total Disk total in bytes\n"
        metrics += f"# TYPE enclave_disk_total gauge\n"
        metrics += f"enclave_disk_total {data['disk_total']}\n"

        if "oracle_metrics" in data:
            for key, value in data["oracle_metrics"].items():
                metrics += f"# HELP {key} {key}\n"
                metrics += f"# TYPE {key} counter\n"
                metrics += f"{key} {value}\n"
    else:
        fetch_metrics_failures_count += 1
    metrics += "# HELP enclave_running Whether the Enclave is up and running\n"
    metrics += "# TYPE enclave_running gauge\n"
    metrics += f"enclave_running {enclave_running}\n"
    metrics += "# HELP enclave_fetch_metrics_failures_total Total number of times the metrics fetch has failed\n"
    metrics += "# TYPE enclave_fetch_metrics_failures_total counter\n"
    metrics += f"enclave_fetch_metrics_failures_total {fetch_metrics_failures_count}\n"
    return metrics


def _get_cid():
    """
    Determine CID of Current Enclave
    """
    try:
        proc = subprocess.Popen(
            ["/bin/nitro-cli", "describe-enclaves"], stdout=subprocess.PIPE
        )
        output = json.loads(proc.communicate()[0].decode())
        enclave_cid = output[0]["EnclaveCID"]
        return enclave_cid
    except:
        return None


@app.get("/metrics", response_class=PlainTextResponse)
def get_metrics():
    data = _get_enclave_metrics()
    return _format_metrics(data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9101)

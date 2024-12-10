import socket
import json
import base64

import psutil 
from NsmUtil import NSMUtil
import key_manager
from proxy_checks import openai_call


def main():
    print("Starting server...")

    # Initialise NSMUtil
    nsm_util = NSMUtil()

    # Create a vsock socket object
    client_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)

    # Listen for connection from any CID
    cid = socket.VMADDR_CID_ANY

    # The port should match the client running in parent EC2 instance
    client_port = 5000

    # Bind the socket to CID and port
    client_socket.bind((cid, client_port))

    # Listen for connection from client
    client_socket.listen()

    while True:
        client_connection, addr = client_socket.accept()

        # Get command from client
        payload = client_connection.recv(4096)
        request = json.loads(payload.decode())

        if request["action"] == "ping":
            response = json.dumps({
                "ping": "pong"
            })
            client_connection.send(str.encode(response))
        elif request["action"] == "check_openai_proxy":
            openai_is_success, openai_error = openai_call.execute()
            response = json.dumps({
                "success": openai_is_success,
                "error": openai_error
            })
            client_connection.send(str.encode(response))
        elif request["action"] == "get_attestation_doc":
            # Generate attestation document
            attestation_doc = nsm_util.get_attestation_doc()
            # Base64 encode the attestation doc
            attestation_doc_b64 = base64.b64encode(attestation_doc).decode()
            attestation_doc_response = json.dumps({
                "attestation_doc_b64": attestation_doc_b64
            })
            client_connection.send(str.encode(attestation_doc_response))
        elif request["action"] == "send_secrets":
            secrets = request["secrets"]
            print("secrets:", secrets)
            dot_env = secrets["dot_env"]
            key_manager.save_dot_env(dot_env)
            gcp_creds_json = secrets["gcp_creds_json"]
            key_manager.save_gcp(gcp_creds_json)
            response = json.dumps({
                "result": "OK"
            })
            client_connection.send(str.encode(response))
        elif request["action"] == "sign_message":
            try:
                message = request["message"]
                signed_message = nsm_util.sign_message(message)
                request = json.dumps({
                    "signed_message": signed_message
                })
                client_connection.send(str.encode(request))
            except Exception as exc:
                client_connection.send(str.encode(json.dumps({
                    "exception": str(exc)
                })))
        elif request["action"] == "dns":
            hostname = request["hostname"]
            try:
                ip_address = socket.gethostbyname(hostname)
                request = json.dumps({
                    "ip_address": ip_address,
                    "error": ""
                })
            except socket.error as e:
                request = json.dumps({
                    "ip_address": "",
                    "error": str(e)
                })
            client_connection.send(str.encode(request))
        elif request["action"] == "ps":
            cpu_usage = psutil.cpu_percent(percpu=True)
            memory_usage = psutil.virtual_memory()
            disk_usage = psutil.disk_usage('/')
            response = {}
            response["cpu_count"] = len(cpu_usage)
            response["cpu_usage"] = {}
            for i, usage in enumerate(cpu_usage):
                response[f"cpu_usage"][i] = usage
            response["ram_total"] = memory_usage.total
            response["ram_available"] = memory_usage.available
            response["ram_used"] = memory_usage.used
            response["disk_total"] = disk_usage.total
            response["disk_free"] = disk_usage.free
            response["disk_used"] = disk_usage.used
            response["oracle_metrics"] = _read_metrics()
            client_connection.send(str.encode(json.dumps(response)))
        else:
            client_connection.send(str.encode(json.dumps({
                "error": "unknown action: " + request["action"]
            })))

        # Close the connection with client
        client_connection.close()


def _read_metrics() -> dict:
    try:
        with open("/app/oracles/metrics.json", "r") as f:
            return json.load(f)
    except:
        return {}


if __name__ == "__main__":
    main()

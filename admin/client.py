import socket
import json
import argparse
import subprocess
import time

import settings

ATTESTATION_OUTPUT = "attestation_doc_b64.txt"

ACTION_PING = "ping"
ACTION_GET_ATTESTATION = "get_attestation_doc"
ACTION_SIGN_MESSAGE = "sign_message"
ACTION_SEND_SECRETS = "send_secrets"
ACTION_PS = "ps"
ACTION_CHECK_OPENAI_PROXY = "check_openai_proxy"
ACTION_DNS = "dns"


def save_attestation_b64(attestation_b64):
    with open(ATTESTATION_OUTPUT, "w", encoding="utf-8") as file:
        file.write(attestation_b64)


def _action_ping(s):
    s.send(str.encode(json.dumps({
        "action": ACTION_PING
    })))
    response = s.recv(65536)
    response_decoded = response.decode()
    print("response_decoded:", response_decoded)


def _action_check_openai_proxy(s):
    s.send(str.encode(json.dumps({
        "action": ACTION_CHECK_OPENAI_PROXY
    })))
    response = s.recv(65536)
    response_decoded = response.decode()
    print("response_decoded:", response_decoded)


def _action_get_attestation(s):
    s.send(str.encode(json.dumps({
        "action": ACTION_GET_ATTESTATION
    })))

    # receive the plaintext from the server and print it to console
    response = s.recv(65536)
    attestation_b64 = response.decode()
    print("attestation_b64:", attestation_b64)
    attestation_b64_dict = json.loads(attestation_b64)
    save_attestation_b64(attestation_b64_dict["attestation_doc_b64"])
    print("saved attestation doc to:", ATTESTATION_OUTPUT)


def _action_sign_message(s, message):
    s.send(str.encode(json.dumps({
        "action": ACTION_SIGN_MESSAGE,
        "message": message
    })))
    # receive the plaintext from the server and print it to console
    response = s.recv(65536)
    signature_b64 = response.decode()
    print("signature_b64:", signature_b64)


def _action_dns(s, hostname):
    s.send(str.encode(json.dumps({
        "action": ACTION_DNS,
        "hostname": hostname
    })))
    # receive the plaintext from the server and print it to console
    response = s.recv(65536)
    response_decoded = response.decode()
    print("response_decoded:", response_decoded)


def get_gcp_creds():
    with open("sidekik.json", "r") as file:
        return file.read()


def _action_send_secrets(s):
    s.send(str.encode(json.dumps({
        "action": ACTION_SEND_SECRETS,
        "secrets": {
            "dot_env": settings.get_dot_env(),
            "gcp_creds_json": get_gcp_creds()
        }
    })))
    response = s.recv(65536)
    print("Send secrets response:", response.decode())


def _action_ps(s):
    s.send(str.encode(json.dumps({
        "action": ACTION_PS,
    })))
    response = s.recv(65536)
    metrics = response.decode()
    print("Metrics:", metrics)


def _get_cid():
    """
    Determine CID of Current Enclave
    """
    proc = subprocess.Popen(["/bin/nitro-cli", "describe-enclaves"],
                            stdout=subprocess.PIPE)
    output = json.loads(proc.communicate()[0].decode())
    enclave_cid = output[0]["EnclaveCID"]
    return enclave_cid


def main(cid: str, action: str, message: str = None, hostname: str = None, until_success: bool = False):
    while True:
        try:
            if not cid:
                cid = _get_cid()
            # Create a vsock socket object
            s = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
            s.settimeout(100.0)
            # The port should match the server running in enclave
            port = 5000
            # Connect to the server
            s.connect((cid, port))

            if action == ACTION_PING:
                _action_ping(s)
            elif action == ACTION_GET_ATTESTATION:
                _action_get_attestation(s)
            elif action == ACTION_SIGN_MESSAGE:
                _action_sign_message(s, message)
            elif action == ACTION_SEND_SECRETS:
                _action_send_secrets(s)
            elif action == ACTION_PS:
                _action_ps(s)
            elif action == ACTION_CHECK_OPENAI_PROXY:
                _action_check_openai_proxy(s)
            elif action == ACTION_DNS:
                _action_dns(s, hostname)

            # close the connection
            s.close()
            return True
        except Exception as exc:
            print("Failed to connect, exc:", exc)
            if not until_success:
                return False
            print("Retrying in 3 sec...")
            time.sleep(3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Enclave client.")
    parser.add_argument(
        "--cid",
        type=int,
        help="an EnclaveCID to connect to"
    )
    parser.add_argument(
        '--action',
        type=str,
        default=ACTION_PING,
        choices=[
            ACTION_PING,
            ACTION_GET_ATTESTATION,
            ACTION_SIGN_MESSAGE,
            ACTION_SEND_SECRETS,
            ACTION_PS,
            ACTION_CHECK_OPENAI_PROXY,
            ACTION_DNS,
        ],
        help="action to run"
    )
    parser.add_argument(
        "--message",
        type=str,
        help="message to sign in the enclave"
    )
    parser.add_argument(
        "--hostname",
        type=str,
        help="hostname to resolve in the enclave"
    )
    parser.add_argument(
        "--until_success",
        type=bool,
        help="retries until success",
        default=False
    )

    args = parser.parse_args()
    main(args.cid, args.action, args.message, args.hostname, args.until_success)

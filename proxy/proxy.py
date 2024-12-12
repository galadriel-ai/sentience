import socket
import threading
import json
import subprocess

BUFFER_SIZE = 4096
HOST = "127.0.0.1"
PORT = 5000
VSOCK_PORT = 5000


def _get_cid():
    """
    Determine CID of Current Enclave
    """
    proc = subprocess.Popen(
        ["/bin/nitro-cli", "describe-enclaves"], stdout=subprocess.PIPE
    )
    output = json.loads(proc.communicate()[0].decode())
    enclave_cid = output[0]["EnclaveCID"]
    return enclave_cid


def forward_data(src_socket, dst_socket):
    """
    Forward data from one socket to another in chunks.
    """
    try:
        while True:
            data = src_socket.recv(BUFFER_SIZE)
            if not data:
                break
            dst_socket.sendall(data)
    except Exception as e:
        print(f"Data forwarding error: {e}")
    finally:
        src_socket.close()
        dst_socket.close()


def _handle_client(cid, client_socket):
    """
    Handle a single client connection, forwarding the data to the VSOCK server and back.
    """
    try:
        # Create a VSOCK socket and connect to the VSOCK server
        vsock_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        vsock_socket.connect((cid, VSOCK_PORT))

        # Start two threads to forward data in both directions
        threading.Thread(
            target=forward_data, args=(client_socket, vsock_socket)
        ).start()
        threading.Thread(
            target=forward_data, args=(vsock_socket, client_socket)
        ).start()
    except Exception as e:
        print(f"Error handling client: {e}")
        client_socket.close()


def main():
    cid = _get_cid()
    # Create a regular TCP socket to listen for HTTP requests
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(
        f"Proxy listening on {HOST}:{PORT}, forwarding to enclave {cid} port {VSOCK_PORT}"
    )

    while True:
        # Accept a new client connection
        client_socket, addr = server_socket.accept()
        # Handle the client connection in a new thread
        threading.Thread(
            target=_handle_client,
            args=(
                cid,
                client_socket,
            ),
        ).start()


if __name__ == "__main__":
    main()

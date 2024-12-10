import socket
import sys
import threading
import time

BUFFER_SIZE = 1024

REMOTE_CID = 3
REMOTE_PORT_OPENAI = 8001
REMOTE_PORT_SERPER = 8002
REMOTE_PORT_GALADRIEL = 8003
REMOTE_PORT_WINDOWS = 8004
REMOTE_PORT_GOOGLE_STORAGE = 8005
REMOTE_PORT_GOOGLE_OAUTH2 = 8006
REMOTE_PORT_E2B = 8007
REMOTE_PORT_GROQ = 8008
REMOTE_PORT_IPFS = 8009
REMOTE_PORT_PINATA = 8010
REMOTE_PORT_ANTHROPIC = 8011

REMOTE_PORTS = {
    "api.openai.com": REMOTE_PORT_OPENAI,
    "google.serper.dev": REMOTE_PORT_SERPER,
    "devnet.galadriel.com": REMOTE_PORT_GALADRIEL,
    "oaidalleapiprodscus.blob.core.windows.net": REMOTE_PORT_WINDOWS,
    "storage.googleapis.com": REMOTE_PORT_GOOGLE_STORAGE,
    "oauth2.googleapis.com": REMOTE_PORT_GOOGLE_OAUTH2,
    "e2b.dev": REMOTE_PORT_E2B,
    "api.groq.com": REMOTE_PORT_GROQ,
    "galadriel.mypinata.cloud": REMOTE_PORT_IPFS,
    "api.pinata.cloud": REMOTE_PORT_PINATA,
    "api.anthropic.com": REMOTE_PORT_ANTHROPIC,
}


def guess_the_destination_port(data: bytes) -> int:
    # the encoding is not utf-8 nor ascii, so ignoring errors and doing best guess
    text = data.decode('utf-8', errors='ignore')
    print("  text:", text)
    for url, port in REMOTE_PORTS.items():
        if url in text:
            print(f"Got destination port: {port} for url: {url}")
            return port
    # TODO: what if no destination?
    print("Error, did not get a destination port!\n")
    return REMOTE_PORT_OPENAI


def server(local_ip, local_port):
    try:
        dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dock_socket.bind((local_ip, local_port))
        dock_socket.listen(5)

        while True:
            client_socket = dock_socket.accept()[0]
            first_batch = client_socket.recv(BUFFER_SIZE)
            destination_port = guess_the_destination_port(first_batch)

            server_socket = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
            server_socket.connect((REMOTE_CID, destination_port))

            outgoing_thread = threading.Thread(
                target=forward,
                args=(client_socket,
                      server_socket, first_batch))
            incoming_thread = threading.Thread(
                target=forward,
                args=(server_socket,
                      client_socket))

            outgoing_thread.start()
            incoming_thread.start()
    except Exception as exc:
        print("TrafficForwarder exception:", exc)
    finally:
        new_thread = threading.Thread(target=server,
                                      args=(local_ip, local_port))
        new_thread.start()

    return


def forward(source, destination, first_string: bytes = None):
    if first_string:
        destination.sendall(first_string)

    string = ' '
    while string:
        try:
            string = source.recv(BUFFER_SIZE)
            if string:
                destination.sendall(string)
            else:
                source.shutdown(socket.SHUT_RD)
                destination.shutdown(socket.SHUT_WR)
        except Exception as exc:
            print("Exception in forward:", exc)


def main(args):
    local_ip = str(args[0])
    local_port = int(args[1])

    thread = threading.Thread(target=server,
                              args=(local_ip, local_port))
    thread.start()
    print(f"starting forwarder on {local_ip}:{local_port}")
    while True:
        time.sleep(60)


if __name__ == '__main__':
    main(sys.argv[1:])

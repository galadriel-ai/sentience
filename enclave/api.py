import socket

import uvicorn


def main():
    print("Starting server...")

    # Initialise NSMUtil

    # Create a vsock socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Listen for connection from any CID
    cid = socket.VMADDR_CID_ANY

    # The port should match the client running in parent EC2 instance
    client_port = 5000

    # Bind the socket to CID and port
    client_socket.bind((cid, client_port))

    # Listen for connection from client
    client_socket.listen()

    # Obtain the file descriptor
    fd = client_socket.fileno()

    uvicorn.run("app:app", fd=fd)


if __name__ == "__main__":
    main()

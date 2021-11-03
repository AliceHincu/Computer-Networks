"""
The client sends a domain name taken from the command line (Ex: www.google.com) to the server. The server opens a TCP
connection to the IP address corresponding to the received domain name on port 80 (called HTTP-Srv). It sends on the
TCP connection the string: “GET / HTTP/1.0\n\n” and relays the answer back to the client. When HTTP-Srv closes
connection to the server, the server closes the connection to the client at its turn.
"""

import socket
import threading
import struct

HOST = '192.168.43.20'
PORT = 2021
ADDRESS = (HOST, PORT)


def worker(client_socket, client_address):
    print(f"Client has connected with IP: {client_address[0]} and PORT: {client_address[1]}")

    domain_length = struct.unpack("!i", client_socket.recv(4))[0]
    domain = client_socket.recv(domain_length).decode('ascii')

    try:
        host_ip = socket.gethostbyname(domain)
        print(f"Domain {domain} has IP: {host_ip}")

        # The server opens a TCP
        # connection to the IP address corresponding to the received domain name on port 80
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.connect((host_ip, 80))
        message = "GET / HTTP/1.0\n\n"

        # send the message
        new_socket.sendall(bytes(message, 'ascii'))

        finished = False
        while not finished:
            msg = new_socket.recv(100)
            if msg:
                client_socket.send(msg)
            else:
                finished = True
    except socket.error:
        print("Unable to get IP")
    finally:
        client_socket.close()


if __name__ == '__main__':
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(ADDRESS)
        server_socket.listen(4)
        print("Listening...")
    except socket.error as msg:
        print(msg.streror)
        exit(-1)

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=worker, args=(client_socket, client_address), daemon=True)
        client_thread.start()

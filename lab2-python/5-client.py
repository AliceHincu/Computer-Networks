"""
The client sends a domain name taken from the command line (Ex: www.google.com) to the server. The server opens a TCP
connection to the IP address corresponding to the received domain name on port 80 (called HTTP-Srv). It sends on the
TCP connection the string: “GET / HTTP/1.0\n\n” and relays the answer back to the client. When HTTP-Srv closes
connection to the server, the server closes the connection to the client at its turn.
"""


import socket
import struct

HOST = '192.168.43.20'
PORT = 2021
ADDRESS = (HOST, PORT)


if __name__ == '__main__':
    client_socket = None
    try:
        client_socket = socket.create_connection(ADDRESS)
    except socket.error as msg:
        print(msg.strerror)
        exit(-1)

    domain = input("Give domain name: ")
    client_socket.sendall(struct.pack('!i', len(domain)))
    client_socket.sendall(bytes(domain, 'ascii'))

    finished = False
    message = ""
    while not finished:
        msg = client_socket.recv(100)
        if msg:
            message += msg.decode('latin-1')
        else:
            finished = True
    print(message)
    client_socket.close()
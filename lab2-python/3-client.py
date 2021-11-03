# 3.   The server chooses a random float number <SRF>. Run multiple clients. Each client chooses a random float number
# <CRF> and send it to the server. When the server does not receive any incoming connection for at least 10 seconds it
# chooses the client that has guessed the best approximation (is closest) for its own number and sends it back the
# message “You have the best guess with an error of <SRV>-<CRF>”. It also sends to each other client the string
# “You lost !”. The server closes all connections after this.

import socket
import struct

HOST = '192.168.43.20'
PORT = 1234

if __name__ == '__main__':
    client_socket = None
    try:
        client_socket = socket.create_connection((HOST, PORT))
    except socket.error as msg:
        print(msg.strerror)
        exit(-1)

    CRF = float(input("Give random float number: "))
    client_socket.sendall(struct.pack('!f', CRF))

    length = client_socket.recv(4)
    length = struct.unpack("!i", length)[0]
    text = client_socket.recv(length).decode('ascii')
    print(text)


"""
Write a pair of TCP/IP applications (SERVER, CLIENT) where each CLIENT connects to the SERVER on port 7000 over TCP.
The server keeps a list of all connected CLIENTS(ip and port) and sends that list to each CLIENT upon connection.
The server also sends incremental changes to the list to each of the connected CLIENTS whenever a new CLIENT arrives
or when a CLIENT closes its TCP connection to the server.

Each CLIENT reads messages from the standard input and sends that message over UDP to all the other CLIENTS registered
to the server(the list is kept by each CLIENT and updated by the SERVER). Users can type in messages at the standard
input and each message will be sent by the CLIENT to all other registered CLIENTS through UDP. Whenever the user enters
a message with the content 'QUIT' - that CLIENT disconnects its TCP connection from the SERVER and closes its UDP socket
(the 'QUIT' message is not sent to all other clients). Upon receiving a list incremental update, each CLIENT displays
a message stating the client action (Ex. 'Client 192.168.0.3:5000 has disconnected' or 'Client 192.168.0.3:5000 has
connected' )
"""
import select
import socket
import struct
from time import sleep

IP = '192.168.1.6'
PORT = 7000
SERV_ADDR = (IP, PORT)

if __name__ == '__main__':
    tcp_socket = None
    udp_socket = None
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(SERV_ADDR)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # tcp_socket.setblocking(False)
        # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # udp_socket
    except socket.error as msg:
        print("Error: ", msg.strerror)
        exit(-1)

    # RECEIVE THE LIST WITH CONNECTED CLIENTS
    connections = []
    inputs = [tcp_socket]
    connections_count = struct.unpack("!i", tcp_socket.recv(4))[0]

    print("--- Clients already connected: ")
    for _ in range(connections_count):
        ip_len = struct.unpack("!i", tcp_socket.recv(4))[0]
        ip = tcp_socket.recv(ip_len).decode()
        port = struct.unpack("!i", tcp_socket.recv(4))[0]
        connections.append((ip, port))
        print((ip, port))
    print("--- Incoming connections: ")

    while not False:
        r, w, e = select.select(inputs, [], [])
        for sock in r:
            if sock == tcp_socket:
                ip_len = struct.unpack("!i", tcp_socket.recv(4))[0]
                ip = tcp_socket.recv(ip_len).decode()
                port = struct.unpack("!i", tcp_socket.recv(4))[0]
                address = (ip, port)
                if address not in connections:
                    print(address, "connected")
                    connections.append(address)
                else:
                    print(address, "disconnected")
                    connections.append(address)
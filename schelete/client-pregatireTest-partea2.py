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
import threading

IP = '127.0.0.1'
PORT = 7000
SERV_ADDR = (IP, PORT)

finished = False
lock = threading.Lock()
connections = []


def reader(udp_sock):
    global finished, lock, connections

    while not finished:
        msg = input("")
        if msg == 'QUIT':
            lock.acquire()
            finished = True
            lock.release()
        else:
            lock.acquire()
            for connection in connections:
                udp_sock.sendto(struct.pack("!i", len(msg)), connection)
                udp_sock.sendto(msg.encode(), connection)
            lock.release()


if __name__ == '__main__':
    tcp_socket = None
    udp_socket = None
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(SERV_ADDR)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # tcp_socket.setblocking(False)
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind(tcp_socket.getsockname())
        # udp_socket.setblocking(False)
    except socket.error as msg:
        print("Error: ", msg.strerror)
        exit(-1)

    # RECEIVE THE LIST WITH CONNECTED CLIENTS

    connections_count = struct.unpack("!i", tcp_socket.recv(4))[0]

    print("--- Clients already connected: ")
    for _ in range(connections_count):
        ip_len = struct.unpack("!i", tcp_socket.recv(4))[0]
        ip = tcp_socket.recv(ip_len).decode()
        port = struct.unpack("!i", tcp_socket.recv(4))[0]
        connections.append((ip, port))
        print((ip, port))
    print("--- Incoming connections: ")

    # READER THREAD
    reader_thread = threading.Thread(target=reader, args=(udp_socket, ))
    reader_thread.start()
    inputs = [tcp_socket, udp_socket]

    lock.acquire()  # for finished
    while not finished:
        lock.release()
        r, w, e = select.select(inputs, [], [], 1)
        for sock in r:
            if sock == tcp_socket:
                ip_len = struct.unpack("!i", tcp_socket.recv(4))[0]
                ip = tcp_socket.recv(ip_len).decode()
                port = struct.unpack("!i", tcp_socket.recv(4))[0]
                address = (ip, port)
                if address not in connections:
                    print(address, "connected")
                    lock.acquire()
                    connections.append(address)
                    lock.release()
                else:
                    print(address, "disconnected")
                    lock.acquire()
                    connections.remove(address)
                    lock.release()
            if sock == udp_socket:
                size = struct.unpack("!i", udp_socket.recvfrom(4)[0])[0]
                text, address = udp_socket.recvfrom(size)
                print(address, ":", text)
        lock.acquire()
    lock.release()
    tcp_socket.close()
    udp_socket.close()

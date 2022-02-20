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

IP = '0.0.0.0'
PORT = 7000
SERV_ADDR = (IP, PORT)


def send_all_clients(server, sockets, address):
    # Send to all the clients the new connection
    for client in sockets:
        if client != server:
            ip = address[0]
            port = address[1]
            client.send(struct.pack("!i", len(ip)))
            client.send(bytes(address[0], 'ascii'))
            client.send(struct.pack("!i", port))


def send_client_all_addresses(client, addresses):
    # Send to the new client all the other clients
    client.send(struct.pack("!i", len(addresses)))
    for address in addresses:
        ip = address[0]
        port = address[1]
        client.send(struct.pack("!i", len(ip)))
        client.send(bytes(address[0], 'ascii'))
        client.send(struct.pack("!i", port))


if __name__ == '__main__':
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(SERV_ADDR)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # server_socket.setblocking(False)
        server_socket.listen(6)
        print("Listening...")
    except socket.error as msg:
        print("Error: ", msg.strerror)
        exit(-1)

    clients = []
    inputs = [server_socket]
    while True:
        r, w, e = select.select(inputs, [], [])
        for sock in r:
            if sock == server_socket:
                new_client_socket, new_client_address = server_socket.accept()
                print("New client: ", new_client_address)
                send_all_clients(server_socket, inputs, new_client_address)
                send_client_all_addresses(new_client_socket, clients)
                inputs.append(new_client_socket)
                clients.append(new_client_address)
            else:
                try:
                    data = sock.recv(4)
                    if not data:
                        addr = sock.getpeername()
                        print("Client closed: ", addr)
                        inputs.remove(sock)
                        clients.remove(addr)
                        send_all_clients(server_socket, inputs, addr)
                        sock.close()

                except socket.error as msg:
                    addr = sock.getpeername()
                    print("Client forcibly hung: ", addr)
                    inputs.remove(sock)
                    clients.remove(addr)
                    send_all_clients(server_socket, inputs, addr)
                    sock.close()
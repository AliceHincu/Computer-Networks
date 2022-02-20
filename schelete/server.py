import pickle
import select
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('0.0.0.0', 7000)
server.bind(address)
print('Starting up on %s port %s' % address)

input_sockets = [server]
output_sockets = []
clients = []

server.listen(10)
i = 0

while True:
    readable, writable, exceptional = select.select(input_sockets, output_sockets, input_sockets)

    for s in readable:

        if s is server:

            i = i+1
            client_socket, client_address = s.accept()
            print('New connection from client ' + str(i) + ' with address: ' + str(client_address))

            client_socket.send(pickle.dumps(clients))
            for client in input_sockets:
                if client is not server:
                    client.send(pickle.dumps(client_address))

            input_sockets.append(client_socket)
            clients.append(client_address)

        else:

            client_address = s.getpeername()
            print("Client with address '" + str(client_address) + "' disconnected")
            clients.remove(client_address)
            input_sockets.remove(s)

            for client in input_sockets:
                if client is not server:
                    client.send(pickle.dumps(client_address))

            s.close()

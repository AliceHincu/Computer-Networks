import socket, random, pickle, time

port = random.randint(1000, 10000)
server_address = ('127.0.0.1', 7000)

own_address = ('127.0.0.1', port)

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind(own_address)

message, server_addr = server_sock.recvfrom(1000)
print(pickle.loads(message))

guessed = False

while not guessed:
    guess = random.randint(1, 100)
    server_sock.sendto(pickle.dumps(guess), server_addr)

    data, addr = server_sock.recvfrom(100)
    message = pickle.loads(data)

    print(guess, message)

    if message != 'S' and message != 'B':
        guessed = True
    
    time.sleep(.25)
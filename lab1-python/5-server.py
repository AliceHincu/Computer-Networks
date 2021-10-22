# 5. The client sends to the server an integer. The server returns the list of divisors for the specified number.

import socket
import struct
# HOST = '127.0.0.1'  localhost
# HOST = '192.168.43.20'  # hot spot
HOST = '192.168.1.3'  # wi fi digi
PORT = 3000


def divisors_of(n):
    divs = []
    for i in range(1, n+1):
        if n % i == 0:
            divs.append(i)

    return divs


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(2)
    print("Listening...")
    conn, addr = sock.accept()
    with conn:
        print("Connected with ", addr)

        data = struct.unpack("!q", conn.recv(100))[0]
        print("Received number: ", data)

        divs = divisors_of(data)
        conn.send(str(divs).encode())
        print("Sent the divisors: ", divs)
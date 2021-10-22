#!/usr/bin/env python3

import socket
import struct

# HOST = '127.0.0.1'  localhost
# HOST = '192.168.43.20'  # hot spot
HOST = '192.168.1.3'  # wi fi digi
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.connect((HOST, PORT))
    except socket.error:
        print("Error connecting")
        exit(-1)
    print("Connected to server.")

    number = int(input("Give number: "))
    sock.send(struct.pack("!q", number))

    divs = sock.recv(100)
    divs = eval(divs.decode())
    print("Divisors: ", divs)
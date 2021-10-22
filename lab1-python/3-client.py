#!/usr/bin/env python3

import socket
import struct

HOST = '192.168.1.3'
# HOST = '192.168.43.20'  # hot spot
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        sock.connect((HOST, PORT))
    except socket.error:
        print("Error connecting")
        exit(-1)
    print("Connected to server.")

    string = input("Give the string: ").encode()
    sock.send(string)

    # it sends a tuple with a single element(ex: (5,)) that is why we need [0]
    data = sock.recv(100).decode()
    print(data)
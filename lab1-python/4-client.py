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

    array1 = input("Give first list of chars: ")
    array1 = [i for i in array1.split()]

    array2 = input("Give second list of chars: ")
    array2 = [i for i in array2.split()]

    sock.send(str(array1).encode())
    sock.send(str(array2).encode())

    array3 = sock.recv(100).decode()
    array3 = eval(array3)
    print(array3)

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
    character = input("Give character: ").encode()

    sock.send(string)
    sock.send(struct.pack("!c", character))

    string_positions = sock.recv(100).decode()
    list_positions = eval(string_positions)
    print("Locations of character ", character, "in string: ", list_positions)


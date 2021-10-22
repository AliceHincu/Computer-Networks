#!/usr/bin/env python3

import socket

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
    array = input("Give the array:")
    aList = [int(i) for i in array.split()]

    # Convert To String and encode it
    aList = str(aList).encode()
    # Send Encoded String version of the List
    sock.send(aList)
    print("Array sent")

    data = sock.recv(100)
    print("Sum received:")
    sum = data.decode('utf-8')
    print(sum)
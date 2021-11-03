"""
 The clients send an integer number N and an array of N float values. The server will merge sort the numbers received
 from all clients until it gets an empty array of floats (N=0). The server returns to each client the size of the
 merge-sorted array followed by the merge-sorted arrays of all floats from all clients.
"""
import socket
import struct

HOST = '192.168.1.6'
PORT = 2021
ADDRESS = (HOST, PORT)


if __name__ == '__main__':
    client_socket = None
    try:
        client_socket = socket.create_connection(ADDRESS)
    except socket.error as msg:
        print(msg.strerror)
        exit(-1)

    size = int(input("Give array size: "))
    client_socket.sendall(struct.pack('!i', size))
    if size != 0:
        print("Give array: ")
        for _ in range(size):
            float_number = float(input(">>"))
            client_socket.sendall(struct.pack('!f', float_number))

    array_dimension = struct.unpack("!i", client_socket.recv(4))[0]
    array_sorted = []
    if array_dimension == 0:
        print("There is no array")
    else:
        for i in range(array_dimension):
            array_number = struct.unpack("!f", client_socket.recv(4))[0]
            array_sorted.append(array_number)
        print("RECEIVED! ")
        print(f"Array size: {array_dimension}")
        print(f"Array: {array_sorted}")
        client_socket.close()
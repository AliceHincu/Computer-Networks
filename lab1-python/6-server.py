# 6. The client sends to the server a string and a character. The server returns to the client a list of all positions
# in the string where specified character is found.

import socket
import struct

# HOST = '127.0.0.1'  localhost
# HOST = '192.168.43.20'  # hot spot
HOST = '192.168.1.3'  # wi fi digi
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    print("Listening...")
    conn, addr = sock.accept()

    with conn:
        print('Connected by', addr)

        string = conn.recv(100).decode()
        character = struct.unpack("!c", conn.recv(1))[0].decode()
        print("You sent the string: ", string, " and the character: ", character)

        positions = [pos for pos, value in enumerate(string) if character == value]
        conn.sendall(str(positions).encode())
        print("List of positions: ", positions)


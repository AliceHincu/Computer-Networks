# 2. A client sends to the server a string. The server returns the count of spaces in the string.
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
        while True:
            data = conn.recv(4096)
            if not data:
                break

            # Decode received data into UTF-8
            data = data.decode('utf-8')
            print("Received from client the string:", data)

            whitespaces = data.count(" ")

            # The form '!' represents the network byte order which is always big-endian as defined in IETF RFC 1700.
            # q means long long
            conn.send(struct.pack("!q", whitespaces))
            print("Sent to client the number of spaces: ", whitespaces)

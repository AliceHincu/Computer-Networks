#  3. A client sends to the server a string. The server returns the reversed string to the client (characters from the
#  end to begging)

import socket
# HOST = '127.0.0.1'  localhost
# HOST = '192.168.43.20'  # hot spot
HOST = '192.168.1.3'  # wi fi digi
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(2)
    print("Listening...")
    # conn = client_socket, addr = (HOST, port)
    conn, addr = sock.accept()

    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(100)
            if not data:
                break

            # Decode received data into UTF-8
            data = data.decode('utf-8')
            print("Received from client the string:", data)

            reversed_string = data[::-1]
            conn.send(reversed_string.encode('utf-8'))
            print("Sent the reversed string: ", reversed_string)

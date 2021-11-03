# 2.   The client sends the complete path to a file. The server returns back the length of the file and its content in
# the case the file exists. When the file does not exist the server returns a length of -1 and no content. The client
# will store the content in a file with the same name as the input file with the suffix –copy appended
# (ex: for f.txt => f.txt-copy).

import socket
import struct
import threading
import pathlib

HOST = '192.168.43.20'
PORT = 1234


def worker(client_socket, client_addr):
    # N, COMMAND       N = len(COMMAND)    .pack   .send
    print("New connection from this client: IP-> ", client_addr[0], " and PORT-> ", client_addr[1])
    length = client_socket.recv(4)
    length = struct.unpack("!i", length)[0]  # decoding
    file_path = client_socket.recv(length)
    file_path = file_path.decode('ascii')
    print("File path sent: ", file_path)

    file_path = pathlib.Path(file_path)
    size = None
    content = None
    if file_path.is_file():
        with file_path.open() as file:
            size = file_path.stat().st_size
            content = file.read()
            client_socket.sendall(struct.pack('!i', size))
            client_socket.sendall(bytes(content, 'ascii'))
    else:
        client_socket.sendall(struct.pack('!i', -1))


    client_socket.close()


if __name__ == '__main__':
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print("Listening...")
    except socket.error as msg:
        print(msg.strerror)
        exit(-1)

    while True:
        client_socket, client_addr = server_socket.accept()
        thread = threading.Thread(target=worker, args=(client_socket, client_addr))
        thread.start()

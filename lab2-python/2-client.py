# 2.   The client sends the complete path to a file. The server returns back the length of the file and its content in
# the case the file exists. When the file does not exist the server returns a length of -1 and no content. The client
# will store the content in a file with the same name as the input file with the suffix –copy appended
# (ex: for f.txt => f.txt-copy).

import socket
import struct
from sys import argv

HOST = '192.168.43.20'
PORT = 1234


if __name__ == '__main__':
    client_socket = None
    try:
        client_socket = socket.create_connection((HOST, PORT))
    except socket.error as msg:
        print("Error: ", msg.strerror)
        exit(-1)

    # i will not input this :\
    path = "C:\\Users\\Sakura\\Desktop\\Facultate\\lab2reteleExample1.txt"
    # path = "C:\\Users\\Sakura\\Desktop\\Facultate\\vdvdf.txt"

    print("The path that was send is: ", path)

    length = len(path)
    length = struct.pack("!i", length)
    client_socket.sendall(length)
    client_socket.sendall(bytes(path, 'ascii'))

    file_path_copy = path[:-4] + "-copy.txt"

    file_length = client_socket.recv(4)
    file_length = struct.unpack('!i', file_length)[0]
    if file_length == -1:
        print("The file does not exist")
    else:
        print("The file exists and has the length: ", file_length)
        content = client_socket.recv(file_length)
        with open(file_path_copy, 'wb') as file:
                file.write(content)

    client_socket.close()


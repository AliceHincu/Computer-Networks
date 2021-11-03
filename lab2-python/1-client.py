#  The client takes a string from the command line and sends it to the server.
#  The server interprets the string as a command with its parameters. It executes the command and returns the
#  standard output and the exit code to the client.

# dir, mkdir test, rmdir test, rename test hope-test-2, netstat -ano, findstr ":8080"

import socket
import struct
from sys import argv

HOST = '192.168.43.20'
PORT = 1234


# Function to convert
def listToString(arguments):
    arguments = arguments[1:]
    string = ""

    # traverse in the string
    for elements in arguments:
        string += elements + " "

    # return string
    return string


if __name__ == '__main__':
    client_socket = None
    try:
        client_socket = socket.create_connection((HOST, PORT))
    except socket.error as msg:
        print("Error: ", msg.strerror)
        exit(-1)

    command = listToString(argv)
    length = len(command)
    print("The command that was send is: ", command)

    length = struct.pack("!i", length)
    client_socket.sendall(length)
    client_socket.sendall(bytes(command, 'ascii'))

    exit_code = struct.unpack("!i", client_socket.recv(4))[0]
    len_content = struct.unpack("!i", client_socket.recv(4))[0]
    content = client_socket.recv(len_content).decode('ascii')

    print("Exit code: ", exit_code)
    print("Content: ", content)
    client_socket.close()







#  The client takes a string from the command line and sends it to the server.
#  The server interprets the string as a command with its parameters. It executes the command and returns the
#  standard output and the exit code to the client.

# dir, mkdir test, rmdir test, rename test hope-test-2, netstat -ano, findstr ":8080"

import socket
import struct
import threading
import os

HOST = '192.168.43.20'
PORT = 1234


def worker(client_socket, client_addr):
    # N, COMMAND       N = len(COMMAND)    .pack   .send
    print("New connection from this client: IP-> ", client_addr[0], " and PORT-> ", client_addr[1])
    length = client_socket.recv(4)
    print("Length before decoding: ", length)
    length = struct.unpack("!i", length)
    print("Length after decoding: ", length)
    length = length[0]
    command = client_socket.recv(length)
    print("Command before decoding: ", command)
    command = command.decode('ascii')
    print("Command after decoding: ", command)

    # do command . In windows can't avoid error, you need to use subprocess.Popen in linux
    # p = os.popen(command)
    # standard_output = p.read()
    # exit_code = p.close()
    # print("Exit code: ", exit_code)
    #print("Stout: ", standard_output)

    # ca sa mearga cu subprocess pe windows dar nu e bine cu shell = true ca cica invoca ceva mistery program
    from subprocess import Popen, PIPE

    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    stdout = process.communicate()[0]
    exit_code = process.returncode
    # print("Exit code: ", process.returncode, "\nContent: ", stdout.decode('ascii'))

    client_socket.sendall(struct.pack("!i", exit_code))
    client_socket.sendall(struct.pack("!i", len(stdout)))
    client_socket.sendall(stdout)


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

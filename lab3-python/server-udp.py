import socket

IP = '192.168.1.6'
PORT = 2021
ADDR = (IP, PORT)
BUFFER_SIZE = 1024

if __name__ == '__main__':
    msgFromServer = "Hello client!"
    server_socket = None
    try:
        server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(ADDR)
    except socket.error as msg:
        print("Error: ", msg.strerror)
        exit(-1)

    print("UDP server up and listening")
    while True:
        pair = server_socket.recvfrom(BUFFER_SIZE)
        message = pair[0].decode()
        address = pair[1]

        print(f"Message from Client with address {address}: {message}")

        server_socket.sendto(msgFromServer.encode(), address)
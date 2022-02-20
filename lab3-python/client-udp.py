import socket

IP = '192.168.1.6'
PORT = 2021
ADDR = (IP,PORT)
BUFFER_SIZE = 1024

if __name__ == '__main__':
    msgFromClient = "Hello UDP Server!"
    client_socket = None
    try:
        client_socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except socket.error as msg:
        print("Error: ", msg.strerror)
        exit(-1)

    client_socket.sendto(msgFromClient.encode(), ADDR)
    pair = client_socket.recvfrom(BUFFER_SIZE)
    message = pair[0].decode()
    address = pair[1]
    print(f"Message from SERVER with address {address}: {message}")
    client_socket.close()
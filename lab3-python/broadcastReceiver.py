import socket

IP = '' # to not use the machine ip...it is equivalent to INADDR_ANY
PORT = 2021
ADDR = (IP, PORT)
BUFFER_SIZE = 1024

if __name__ == '__main__':
    receiver_socket = None
    try:
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        receiver_socket.bind(ADDR)
    except socket.error as msg:
        print(f"Error: {msg.strerror}")
        exit(-1)

    pair = receiver_socket.recvfrom(BUFFER_SIZE)
    message = pair[0].decode()
    address = pair[1]
    print(f"Received message from {ADDR} : {message}")

    sendMSG = "Broadcast message from a RECEIVER"
    receiver_socket.sendto(sendMSG.encode(), address)


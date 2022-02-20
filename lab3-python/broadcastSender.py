import socket

IP = '192.168.1.255'  # OR '<broadcast>' -> ask which we are allowed to use(+receiver)
PORT = 2021
ADDR = (IP, PORT)
BUFFER_SIZE = 1024

if __name__ == '__main__':
    sender_socket = None
    try:
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    except socket.error as msg:
        print(f"Error: {msg.strerror}")
        exit(-1)

    sendMSG = "Broadcast message from SENDER"
    sender_socket.sendto(sendMSG.encode(), ADDR)

    for _ in range(3):
        pair = sender_socket.recvfrom(BUFFER_SIZE)
        message = pair[0].decode()
        address = pair[1]

        print(f"Message from Client with address {address}: {message}")

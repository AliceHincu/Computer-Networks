import random
import socket
import struct
import time

IP = '192.168.1.6'
PORT = 7000
SERV_ADDR = (IP, PORT)

if __name__ == '__main__':
    client_sock = None
    try:
        client_sock = socket.create_connection(SERV_ADDR)
    except socket.error as msg:
        print("Error: ", msg.strerror)
        exit(-1)

    size = struct.unpack("!i", client_sock.recv(4))[0]
    message = client_sock.recv(size)
    print(message.decode('ascii'))
    number_of_digits = struct.unpack("!i", client_sock.recv(4))[0]
    print(number_of_digits)

    step_count = 0
    finished = False

    while not finished:
        my_digit = random.randint(0, 9)
        print(f"My digit is: {my_digit}")

        try:
            client_sock.sendall(struct.pack("!i", my_digit))
            size = struct.unpack("!i", client_sock.recv(4))[0]
        except socket.error as msg:
            print("Error: ", msg.strerror)
            client_sock.close()
            exit(-2)

        if size > 0:
            positions = []
            for _ in range(size):
                pos = struct.unpack("!i", client_sock.recv(4))[0]
                positions.append(pos)
            print(f"Digit found on positions: {positions}")
        if size == 0:
            print("Digit is not in the number")
        if size == -1:
            print("You win!")
            finished = True
        if size == -2:
            print("You lose!")
            finished = True

        time.sleep(1)

    client_sock.close()
import socket
import random
import struct
import time

HOST = '192.168.1.3'
PORT = 1234

if __name__ == '__main__':
    try:
        client_sock = socket.create_connection((HOST, PORT))
    except socket.error as msg:
        print("Error: ", msg.strerror)
        exit(-1)

    finished = False
    left_interval = 1
    right_interval = 2**17-1
    random.seed()

    message = client_sock.recv(1024)
    print(message.decode('ascii'))
    step_count = 0

    while not finished:

        my_num = random.randint(left_interval, right_interval)
        print(my_num, ": (", left_interval, ", ", right_interval, ")")
        try:

            client_sock.sendall(struct.pack("!I", my_num))
            answer = client_sock.recv(1)
        except socket.error as msg:
            print("Error: ", msg.strerror)
            socket.close()
            exit(-2)

        step_count += 1
        print("Sent: ", my_num, " Answer: ", answer.decode('ascii'))
        if answer == b'H':
            left_interval = my_num
        if answer == b'S':
            right_interval = my_num
        if answer == b'G' or answer == b'L':
            finished = True
        time.sleep(0.25)

    client_sock.close()
    if answer == b'G':
        print("I am the winner with number: ", my_num, " and i guessed it in ", step_count, " steps")
    else:
        print("I lost!")

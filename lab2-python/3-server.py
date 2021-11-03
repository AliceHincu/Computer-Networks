# 3.   The server chooses a random float number <SRF>. Run multiple clients. Each client chooses a random float number
# <CRF> and send it to the server. When the server does not receive any incoming connection for at least 10 seconds it
# chooses the client that has guessed the best approximation (is closest) for its own number and sends it back the
# message “You have the best guess with an error of <SRV>-<CRF>”. It also sends to each other client the string
# “You lost !”. The server closes all connections after this.

import socket
import threading
import random
import struct


lock = threading.Lock()
threads = {}  # key: client socket. values: client thread and crf

HOST = '192.168.43.20'
PORT = 1234
SRF = 0
client_count = 0
delay_time = 10


def random_float_number():
    random.seed()
    start = 0.0
    end = 100.0
    my_num = random.uniform(start, end)
    return my_num


def worker(client_socket, client_address):
    global client_count

    my_id = client_count
    print(">>>New connection from client #", my_id, ": IP-> ", client_address[0],
          " and PORT-> ", client_address[1])
    CRF = struct.unpack('!f', client_socket.recv(4))[0]
    print("Client #", my_id, "sent the number: ", CRF)

    threads[client_socket][1] = CRF


def treat_clients():
    global threads, my_num
    closest_client_socket = None
    closest_client_diff = None

    lock.acquire()
    for client_socket, (client_thread, CRF) in threads.items():
        if closest_client_diff is None or SRF - CRF < closest_client_diff:
            closest_client_diff = SRF - CRF
            closest_client_socket = client_socket
    text = ""
    for client_socket in threads.keys():
        if client_socket == closest_client_socket:
            text = "You have the best guess with an error of " + str(closest_client_diff)
        else:
            text = "You lost! :("
        client_socket.sendall(struct.pack("!i", len(text)))
        client_socket.sendall(bytes(text, 'ascii'))
        client_socket.close()


if __name__ == '__main__':
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(4)
        print("Listening...")
    except socket.error as msg:
        print(msg.strerror)
        exit(-1)

    SRF = random_float_number()
    print("The server number is: ", SRF)

    finished = False

    while not finished:
        try:
            server_socket.settimeout(delay_time)
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=worker, args=(client_socket, client_address), daemon=True)

            lock.acquire()
            client_count += 1
            threads[client_socket] = [client_thread, None]
            lock.release()

            client_thread.start()
        except socket.error as msg:
            print("Time has passed!")
            treat_clients()
            finished = True
        finally:
            server_socket.settimeout(None)


    server_socket.close()
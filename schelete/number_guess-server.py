import socket
import threading
import struct
import random
import time

HOST = '192.168.1.3'
PORT = 1234
threads = []
client_count = 0
client_guessed = False
my_lock = threading.Lock()
winner_thread = 0

random.seed()
start = 1
stop = 2**17-1
my_num = random.randint(start, stop)

e = threading.Event()
e.clear()


def resetServ():
    global threads, client_guessed, winner_thread, my_num, threads,e, client_count
    while True:
        print(my_num)
        e.wait()
        for t in threads:
            t.join()
        print("all threads are finished now")
        e.clear()

        my_lock.acquire()
        threads = []
        client_guessed = False
        winner_thread = -1
        client_count = 0
        my_num = random.randint(start, stop)
        print('Server number: ', my_num)
        my_lock.release()


def worker(client_sock):
    global my_lock, client_count, client_guessed, my_num, winner_thread

    my_id_count = client_count
    print("Client #", str(my_id_count), "from:", client_sock.getpeername(), client_sock)
    message = "Hello client #" + str(my_id_count) + " ! You are entering the number guess competition now."
    client_sock.sendall(bytes(message, 'ascii'))

    while not client_guessed:
        try:
            client_number = client_sock.recv(4)
            client_number = struct.unpack("!I", client_number)[0]
            if client_number > my_num:
                client_sock.sendall(b'S')
            if client_number < my_num:
                client_sock.sendall(b'H')
            if client_number == my_num:
                my_lock.acquire()
                client_guessed = True
                winner_thread = threading.get_ident()
                my_lock.release()
        except socket.error as msg:
            print('Error:', msg.strerror)
            break

    if client_guessed:
        if threading.get_ident() == winner_thread:
            client_sock.sendall(b'G')
            print("We have a winner", client_sock.getpeername())
            print("Thread ", my_id_count, "  winner")
            e.set()
        else:
            client_sock.sendall(b'L')
            print("Thread ", my_id_count, "  looser")

    time.sleep(1)
    client_sock.close()
    print("Worker Thread ", my_id_count, " end")


if __name__ == '__main__':
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print("Listening...")
    except socket.error as msg:
        print(msg.strerror)
        exit(-1)

    t = threading.Thread(target=resetServ, daemon=True)
    t.start()
    while True:
        client_socket, client_address = server_socket.accept()
        t = threading.Thread(target=worker, args=(client_socket,) )
        threads.append(t)
        client_count += 1
        t.start()

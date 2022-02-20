import socket, pickle
from threading import Thread, Lock
import random

server_address = ('127.0.0.1', 7000)

secret_number = random.randint(1, 100)
guessed = False

lock = Lock()

def handle_client(port):
    global secret_number, guessed, lock

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port + 1))
    sock.sendto(pickle.dumps("hello there"), ('127.0.0.1', port))
    
    tries = 1
    winner = False

    while not guessed:
        data, addr = sock.recvfrom(1000)
        guess = pickle.loads(data)
        reply = ""
        
        lock.acquire()
        if guess < secret_number:
            reply = 'B'
        elif guess > secret_number:
            reply = 'S'
        else:
            reply = 'You won within ' + str(tries) + ' tries'
            guessed = True
            winner = True
        
        sock.sendto(pickle.dumps(reply), addr)

        if guessed:
            lock.release()
            break

        lock.release()
        tries += 1
    
    if not winner:
        sock.sendto(pickle.dumps('You lost within ' + str(tries) + ' tries'), ('127.0.0.1', port))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(server_address)
    s.settimeout(5)

    while True:
        active_threads = []
        while not guessed: 
            try:
                data, addr = s.recvfrom(1000)
                t1 = Thread(target=handle_client, args=(pickle.loads(data),))
                t1.start()
                active_threads.append(t1)
            except socket.timeout:
                pass
        
        for t in active_threads:
            t.join()

        guessed = False
        secret_number = random.randint(1, 100)

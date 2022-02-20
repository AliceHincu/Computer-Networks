import socket
import pickle
import threading
import select


def chat(udp_sock):
    global done
    while not done:
        message = input()
        if message == "QUIT":
            lock1.acquire()
            done = True
            lock1.release()
        else:
            lock2.acquire()
            for client in clients:
                udp_sock.sendto(message.encode('utf-8'), client)
            lock2.release()


done = False
server_address = ('127.0.0.1', 7000)
lock1 = threading.Lock()
lock2 = threading.Lock()

s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s_tcp.connect(server_address)

clients_data = s_tcp.recv(1024)
clients = pickle.loads(clients_data)

s_udp.bind(s_tcp.getsockname())

reading = threading.Thread(target=chat, args=(s_udp,))
reading.start()

lock1.acquire()
while not done:
    lock1.release()
    r, w, e = select.select([s_tcp, s_udp], [], [], 1)
    for s in r:
        if s == s_tcp:
            addr = s_tcp.recv(1024)
            addr = pickle.loads(addr)

            lock2.acquire()
            if addr in clients:
                clients.remove(addr)
                print("Client " + str(addr) + " has disconnected.")
            else:
                clients.append(addr)
                print("Client " + str(addr) + " is now connected.")
            lock2.release()
        if s == s_udp:
            msg, addr = s_udp.recvfrom(1024)
            msg = msg.decode()
            print("[" + str(addr) + "]: " + str(msg))

    lock1.acquire()

lock1.release()
reading.join()
s_tcp.close()
s_udp.close()


"""
 The clients send an integer number N and an array of N float values. The server will merge sort the numbers received 
 from all clients until it gets an empty array of floats (N=0). The server returns to each client the size of the 
 merge-sorted array followed by the merge-sorted arrays of all floats from all clients.
"""

import socket
import threading
import struct

HOST = '192.168.1.6'
PORT = 2021
ADDRESS = (HOST, PORT)

client_count = 0
merge_sorted_array = []
threads = {}

e = threading.Event()
e.clear()
lock = threading.Lock()


def treat_clients(server_socket):
    global merge_sorted_array, threads, client_count
    while True:
        e.wait()
        for _, thread in threads.items():
            thread.join()
        print("All threads are finished now")

        lock.acquire()

        for socket, _ in threads.items():
            socket.send(struct.pack("!i", len(merge_sorted_array)))
            for i in range(len(merge_sorted_array)):
                socket.send(struct.pack("!f", merge_sorted_array[i]))
            socket.close()

        merge_sorted_array = []
        threads = {}
        client_count = 0
        e.clear()
        lock.release()


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        L = arr[:mid]  # Dividing the array elements into 2 halves
        R = arr[mid:]

        merge_sort(L)  # Sorting the first half
        merge_sort(R)  # Sorting the second half

        i = j = k = 0

        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def worker(client_socket, client_address):
    global client_count, closing_client, e, merge_sorted_array
    my_id = client_count

    print(f"Client #{my_id} has connected with IP: {client_address[0]} and PORT: {client_address[1]}")
    client_array = []
    client_array_size = struct.unpack('!i', client_socket.recv(4))[0]

    if client_array_size != 0:
        for _ in range(client_array_size):
            float_number = struct.unpack('!f', client_socket.recv(4))[0]
            client_array.append(float_number)
        print(f"Client #{my_id} send an array with {client_array_size} values which is: {client_array}")

        lock.acquire()
        merge_sorted_array.extend(client_array)
        lock.release()

    else:
        print(f"Client #{my_id} sent an empty array so we stop!")
        lock.acquire()
        merge_sort(merge_sorted_array)
        e.set()
        lock.release()


if __name__ == '__main__':
    server_socket = None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(ADDRESS)
        server_socket.listen(4)
        print("Listening...")
    except socket.error as msg:
        print(msg.strerror)
        exit(-1)

    t = threading.Thread(target=treat_clients, args=(server_socket,), daemon=True)
    t.start()
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=worker, args=(client_socket, client_address), daemon=True)

        lock.acquire()
        client_count += 1
        threads[client_socket] = client_thread
        lock.release()

        client_thread.start()

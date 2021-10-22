# 4. The client send to the server two sorted array of chars. The server will merge sort the two arrays and return the
# result to the client.

import socket
# HOST = '127.0.0.1'  localhost
# HOST = '192.168.43.20'  # hot spot
HOST = '192.168.1.3'  # wi fi digi
PORT = 3000


def mergeArrays(arr1, arr2, n1, n2):
    arr3 = [None] * (n1 + n2)
    i = 0
    j = 0
    k = 0

    # Traverse both array
    while i < n1 and j < n2:
        # Check if current element of first array is smaller than current element of second array. If yes, store first
        # array element and increment first array index. Otherwise do same with second array
        if arr1[i] < arr2[j]:
            arr3[k] = arr1[i]
            k = k + 1
            i = i + 1
        else:
            arr3[k] = arr2[j]
            k = k + 1
            j = j + 1

    # Store remaining elements of first array
    while i < n1:
        arr3[k] = arr1[i]
        k = k + 1
        i = i + 1

    # Store remaining elements of second array
    while j < n2:
        arr3[k] = arr2[j]
        k = k + 1
        j = j + 1

    return arr3


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(2)
    print("Listening...")
    # conn = client_socket, addr = (HOST, port)
    conn, addr = sock.accept()

    with conn:
        print("Connected by", addr)
        while True:
            data1 = conn.recv(100)
            data2 = conn.recv(100)
            if not data1 or not data2:
                break

            # Decode received data into UTF-8 and convert it to array
            array1 = eval(data1.decode('utf-8'))
            array2 = eval(data2.decode('utf-8'))
            print("Received from client the arrays:", array1, array2)

            array3 = mergeArrays(array1, array2, len(array1), len(array2))
            conn.send(str(array3).encode('utf8'))
            print("Sent the merged array: ", array3)
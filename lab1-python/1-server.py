#  A client sends to the server an array of numbers. Server returns the sum of the numbers.
import socket

# HOST = '127.0.0.1'  localhost
# HOST = '192.168.43.20'  # hot spot
HOST = '192.168.1.3'  # wi fi digi
PORT = 3000

#  --- Some error handling
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    print("Listening...")
    conn, addr = sock.accept()

    with conn:
        print('Connected by', addr)

        data = conn.recv(4096)

        # Decode received data into UTF-8 and Convert decoded data into list(eval)
        data = eval(data.decode('utf-8'))
        print("Received from client the list:", data)

        sum = 0
        for number in data:
            sum += number

        res = conn.send(str(sum).encode('utf8'))
        print("Sent to client the sum of list: ", sum)


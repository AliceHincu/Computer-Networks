import threading
import sys

PORT = 7777
BROADCAST = sys.argv[1]

class ClientThread(threading.Thread):
    def __init__(self, value):
        super(ClientThread, self).__init__(name="Client thread " + str(value))
        self.val = value

class ServerThread(threading.Thread):
    def __init__(self):
        super(ServerThread, self).__init__(name="Server thread")

if __name__ == '__main__':
    pass
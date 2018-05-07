import socket
from time import sleep
import threading
import queue
import asyncore
import datetime

def process(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(1)
    global q
    while True:
        c, addr = s.accept()
        size = c.recv(4)
        data = c.recv(int.from_bytes(size, byteorder='little'))
        c.close
        q.put(data.decode())

host = ''
port = 6060
q = queue.Queue()
thread = threading.Thread(target=process, args=(host, port))
thread.daemon = True
thread.start()

while True:
    try:
        print(datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3] + "| "+ q.get(timeout=1))
    except KeyboardInterrupt:
        break
    except queue.Empty:
        pass
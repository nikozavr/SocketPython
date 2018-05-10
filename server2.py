import socket
from time import sleep
from threading import Event, Thread, Timer
from queue import Queue
import time

count = 0
interval = 0.04

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

def timer_call(f_stop, target):
    if not f_stop.is_set():
        Timer(target - time.clock(), timer_call, [f_stop, target+interval]).start()
        work()

def work():
    print("Timer work")

host = ''
port = 6060
q = Queue()

try:
    thread = Thread(target=process, args=(host, port))
    thread.daemon = True
    thread.start()
    f_stop = Event()
    target = time.clock() + interval
    timer_call(f_stop, target)
    while not f_stop.is_set():
        sleep(1)
except KeyboardInterrupt:
    print("Interrupted.")
    f_stop.set()
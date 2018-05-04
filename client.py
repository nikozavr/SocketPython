import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 6060
string = sys.argv[1]
s.connect((host, port))
s.send(sys.getsizeof(string).to_bytes(4,byteorder='little')+string.encode('utf-8'))
s.close()
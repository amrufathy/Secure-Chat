import sys
from Client import Client

_socket = Client(('127.0.0.1', 9000))
_socket.connect()

print('Client connected to', _socket.get_host())

while True:
    print('Server says', _socket.recv())

    sys.stdout.write('>> ')
    _socket.send(str(input()))
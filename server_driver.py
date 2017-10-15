import sys

from Server import Server

server = Server()
server.start(9000)
print('Server is running...')

client = server.accept()
print('Received connection from', client.get_host())

while True:
    sys.stdout.write('>> ')
    client.send(str(input()))

    print('Client:', client.recv())

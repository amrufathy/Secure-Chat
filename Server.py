import socket

from Client import Client


class Server:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allows port to be reused
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self, port):
        self._socket.bind(('127.0.0.1', int(port)))
        self._socket.listen(10)  # 10 connections in queue

    def accept(self):
        client_socket, client_addr = self._socket.accept()
        return Client(client_addr, client_socket)

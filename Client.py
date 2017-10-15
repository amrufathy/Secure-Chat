import socket


class Client:
    def __init__(self, addr, _socket=None):
        self.addr = addr

        if _socket is not None:
            self._socket = _socket
        else:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self._socket.connect(self.addr)
        except socket.error as e:
            print("Error connecting to address", str(e))

    def disconnect(self):
        self._socket.shutdown(socket.SHUT_RDWR)  # shutdown both reading and writing
        self._socket.close()

    def send(self, data):
        assert type(data) == str

        data_length = len(data)
        data_length_str = self.__pad_to_eight_chars(data_length)

        # Send data length to be expected
        self.__send(data_length_str, len(data_length_str))
        # Send data itself
        self.__send(data, data_length)

    def recv(self):
        # First, receive message length
        length = self.__recv(8)

        # return message itself
        return self.__recv(length)

    def __send(self, data, length):
        data_sent_length = 0

        while data_sent_length < length:
            data_sent_partial = self._socket.send(data[data_sent_length:].encode('utf-8'))

            if data_sent_partial == 0:
                print("Connection closed")
                break

            data_sent_length += data_sent_partial

    def __recv(self, length):
        received_data = ''
        length = int(length)

        while len(received_data) < length:
            received_chunk = self._socket.recv(length - len(received_data)).decode('utf-8')

            if not received_chunk or received_chunk == '':
                print("Connection closed")
                break

            received_data += received_chunk

        return received_data

    @staticmethod
    def __pad_to_eight_chars(length):
        length_str = str(length)

        while len(length_str) < 8:
            length_str = '0' + length_str

        return length_str

    def get_host(self):
        return self.addr[0]

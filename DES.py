from Crypto.Cipher import DES


class myDES:
    def __init__(self):
        self._key = '12345678'
        self.__des = DES.new(self._key, DES.MODE_ECB)

    def encrypt(self, text):
        return self.__des.encrypt(text)

    def decrypt(self, text):
        return self.__des.decrypt(text)

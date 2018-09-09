import random
import string

from Crypto.Cipher import DES


class myDES:
    def __init__(self, TYPE):
        letters = string.ascii_letters + string.digits
        letters = letters.replace('\\', '').replace('\'', '').replace('\"', '')

        # self._key = '12345678'
        if TYPE == 1:
            self._key = ''.join(random.SystemRandom().choice(letters) for _ in range(8))
            with open('key.txt', 'w') as f:
                f.write(self._key)
        else:
            with open('key.txt', 'r') as f:
                self._key = f.read()

        self.__des = DES.new(self._key, DES.MODE_ECB)

    def encrypt(self, text):
        return self.__des.encrypt(text)

    def decrypt(self, text):
        return self.__des.decrypt(text)

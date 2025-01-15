import os
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

load_dotenv()

class aes:
    AES_IV = os.getenv("AES_IV").encode()
    AES_KEY = os.getenv("AES_KEY").encode()

    def __init__(self):
        pass

    def encrypt(self, data, key=AES_KEY):
        '''
            Function Description
        '''
        data = data.encode()
        cipher = AES.new(key, AES.MODE_CBC, self.AES_IV)
        padded_data = pad(data, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        return ciphertext
    
    def decrypt(self, data, key=AES_KEY):
        '''
            Function Description
        '''
        cipher = AES.new(key, AES.MODE_CBC, self.AES_IV)
        decrypted_padded_data = cipher.decrypt(data)
        decrypted_data = unpad(decrypted_padded_data, AES.block_size)
        return decrypted_data.decode()
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class rsa:
    def generateKeys(self):
        key = RSA.generate(1024)
        privateKey = key
        publicKey = key.publickey()
        return(publicKey, privateKey)

    def encrypt(self, data, publicKey):
        cipher = PKCS1_OAEP.new(publicKey)
        ciphertext = cipher.encrypt(data.encode())
        return ciphertext

    def decrypt(self, data, privateKey):
        cipher = PKCS1_OAEP.new(privateKey)
        plaintext = cipher.decrypt(data)
        return plaintext.decode("utf-8")
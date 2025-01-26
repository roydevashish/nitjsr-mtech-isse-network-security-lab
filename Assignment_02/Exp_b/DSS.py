from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

def generateKeyPair():
    key = ECC.generate(curve='p256')
    privateKey = key
    publicKey = key.public_key()
    return publicKey, privateKey

def generateSignature(message, privateKey):
    # message = b'I give my permission to order #4355'
    # key = ECC.generate(curve='p256')
    # key = ECC.import_key(open('privkey.der').read())
    h = SHA256.new(message.encode())
    signer = DSS.new(privateKey, 'fips-186-3')
    signature = signer.sign(h)
    return signature

def verifySignature(message, signature, publicKey):
    h = SHA256.new(message.encode())
    verifier = DSS.new(publicKey, 'fips-186-3')
    try:
        verifier.verify(h, signature)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    message = input("Your message plz: ")
    privateKey = ECC.generate(curve='p256')
    publicKey = privateKey.public_key()
    print(publicKey)
    pkey = publicKey.export_key(format='PEM')
    publicKeyOther = ECC.import_key(pkey, curve_name='p256')
    print(publicKeyOther)

    print(publicKeyOther == publicKey)


    signature = generateSignature(message, privateKey)
    # print(signature)

    print(verifySignature(message, signature, publicKeyOther))
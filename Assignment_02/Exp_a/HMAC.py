import os
from Crypto.Hash import HMAC, SHA256
from dotenv import load_dotenv

load_dotenv()

def generate(message: str):
    secret = os.getenv("HMAC_SECRET").encode()
    encodedMessage = message.encode()
    h = HMAC.new(secret, digestmod=SHA256)
    h.update(encodedMessage)
    messageDigest = h.hexdigest()

    return encodedMessage, messageDigest

def verify(encodedMessage, messageDigest):
    secret = os.getenv("HMAC_SECRET").encode()
    h = HMAC.new(secret, digestmod=SHA256)
    h.update(encodedMessage)
    try:
        h.hexverify(messageDigest)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    message = input("Input your message: ")
    encodedMessage, digest = generate(message)
    print(f"{encodedMessage}, {type(digest)}")

    mymessage = input("you messgae plz: ")

    print(verify(mymessage.encode(), digest))
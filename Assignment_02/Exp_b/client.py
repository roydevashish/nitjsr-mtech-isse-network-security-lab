import socket
import TerminalMessage as TM
import DSS as Sign
from Crypto.PublicKey import ECC
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: Create socket.
client = socket.socket()

# Server configuration.
config = {
    "ip": os.getenv("HOST"),
    "port": int(os.getenv("PORT"))
}
serverConfig = (config["ip"], config["port"])

# TODO: Connect to server.
try:
    client.connect(serverConfig)

    # TODO: Receive the public key and import it
    receivedLength = client.recv(4)
    length = int.from_bytes(receivedLength, byteorder='big')
    encodedPublicKey = client.recv(length)
    publicKey = ECC.import_key(encodedPublicKey, curve_name='p256')

    # TODO: Receive the connection successful message and signature.
    receivedLength = client.recv(4)
    length = int.from_bytes(receivedLength, byteorder='big')
    encodedMessage = client.recv(length)

    receivedLength = client.recv(4)
    length = int.from_bytes(receivedLength, byteorder='big')
    encodedMessageSignature = client.recv(length)

    if(Sign.verifySignature(encodedMessage.decode(), encodedMessageSignature, publicKey)):
        TM.PrintTry(True, encodedMessage.decode())
    else:
        # TODO: check a better option other then exit.
        TM.PrintMessage("Error: This message is not from authenticated origin.")
        exit()
except:
    TM.PrintTry(False, "Unable to connect to server.")
    exit()

# TODO: Receive the ask name message and signature.
receivedLength = client.recv(4)
length = int.from_bytes(receivedLength, byteorder='big')
encodedMessage = client.recv(length)

receivedLength = client.recv(4)
length = int.from_bytes(receivedLength, byteorder='big')
encodedMessageSignature = client.recv(length)

if(Sign.verifySignature(encodedMessage.decode(), encodedMessageSignature, publicKey)):
    TM.PrintMessage(encodedMessage.decode())
else:
    # TODO: check a better option other then exit.
    TM.PrintMessage("Error: This message is not from authenticated origin.")
    exit()

# TODO: Take name input.
TM.PrintMessage("Your Name Please: ")
name = input()

# TODO: Send name to the server.
length = len(name.encode()).to_bytes(4, byteorder='big')
client.send(length)
client.send(name.encode())

# TODO: Print the welcome message.
receivedLength = client.recv(4)
length = int.from_bytes(receivedLength, byteorder='big')
encodedMessage = client.recv(length)

receivedLength = client.recv(4)
length = int.from_bytes(receivedLength, byteorder='big')
encodedMessageSignature = client.recv(length)

if(Sign.verifySignature(encodedMessage.decode(), encodedMessageSignature, publicKey)):
    TM.PrintMessage(encodedMessage.decode())
else:
    # TODO: check a better option other then exit.
    TM.PrintMessage("Error: This message is not from authenticated origin.")
    exit()

# TODO: Terminate the connection.
client.close()
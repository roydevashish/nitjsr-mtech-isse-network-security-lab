import socket
import TerminalMessage as TM
import HMAC as H
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

    # TODO: Receive the connection successful message and digest.

    receivedLength = client.recv(4)
    length = int.from_bytes(receivedLength, byteorder='big')
    encodedConnectionSuccessfulMessage = client.recv(length)

    receivedLength = client.recv(4)
    length = int.from_bytes(receivedLength, byteorder='big')
    encodedConnectionSuccessfulMessageDigest = client.recv(length)

    print(encodedConnectionSuccessfulMessage, encodedConnectionSuccessfulMessageDigest )
    if(H.verify(encodedConnectionSuccessfulMessage, encodedConnectionSuccessfulMessageDigest.decode())):
        TM.PrintTry(True, encodedConnectionSuccessfulMessage.decode())
    else:
        # TODO: check a better option other then exit.
        TM.PrintMessage("Error 01: This message is tampered.")
        exit()
except:
    TM.PrintTry(False, "Unable to connect to server.")
    exit()

# TODO: Receive the ask name message and digest.
receivedLength = client.recv(4)
length = int.from_bytes(receivedLength, byteorder='big')
encodedNameMessage = client.recv(length)

receivedLength = client.recv(4)
length = int.from_bytes(receivedLength, byteorder='big')
encodedNameMessageDigest = client.recv(length)

if(H.verify(encodedNameMessage, encodedNameMessageDigest.decode())):
    TM.PrintMessage(encodedNameMessage.decode())
else:
    # TODO: check a better option other then exit.
    TM.PrintMessage("Error: This message is tampered.")
    exit()

# TODO: Take name input.
TM.PrintMessage("Your Name Please: ")
name = input()

# TODO: Send name and digest to the server.
encodedName, nameDigest = H.generate(name)
encodedNameDigest = nameDigest.encode()

length = len(encodedName).to_bytes(4, byteorder='big')
client.send(length)
client.send(encodedName)

length = len(encodedNameDigest).to_bytes(4, byteorder='big')
client.send(length)
client.send(encodedNameDigest)

# TODO: Print the welcome message.

receivedLength = client.recv(4)
length = int.from_bytes(receivedLength, byteorder='big')
encodedWelcomeMessage = client.recv(length)

receivedLength = client.recv(4)
length = int.from_bytes(receivedLength, byteorder='big')
encodedWelcomeMessageDigest = client.recv(length)
if(H.verify(encodedWelcomeMessage, encodedWelcomeMessageDigest.decode())):
    TM.PrintMessage(encodedWelcomeMessage.decode())
else:
    # TODO: check a better option other then exit.
    TM.PrintMessage("Error: This message is tampered.")
    exit()

# TODO: Terminate the connection.
client.close()
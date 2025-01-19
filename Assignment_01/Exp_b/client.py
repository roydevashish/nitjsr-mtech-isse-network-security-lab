import socket
import TerminalMessage as TM
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# TODO: Create socket.
client = socket.socket()

# Server configuration.
config = {
    "ip": "localhost",
    "port": 8080
}
serverConfig = (config["ip"], config["port"])

# TODO: Connect to server.
try:
    client.connect(serverConfig)
    
    # TODO: Receive the connection successful message.
    connectionSuccessfulMessage = client.recv(1024).decode()
    TM.PrintTry(True, connectionSuccessfulMessage)

    # TODO: Receive the RSA public key.
    receivedPublicKey = client.recv(1024)
    publicKey = RSA.import_key(receivedPublicKey)
    TM.PrintTry(True, "Received public key for RSA")
except:
    TM.PrintTry(False, "Unable to connect to server.")
    exit()

# Create object for RSA.
cipher = PKCS1_OAEP.new(publicKey)

# TODO: Receive the ask name message and print.
nameMessage = client.recv(1024).decode()
TM.PrintMessage(nameMessage)

# TODO: Take name input and encrypt the name.
TM.PrintMessage("Your Name Please: ")
name = input()
encryptedName = cipher.encrypt(name.encode())

# TODO: Send encrypted name to the server.
client.send(encryptedName)

# TODO: Print the welcome message.
welcomeMessage = client.recv(1024)
TM.PrintMessage(welcomeMessage.decode())

# TODO: Terminate the connection.
client.close()
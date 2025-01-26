import socket
import TerminalMessage as TM
import DSS as Sign
import os
from dotenv import load_dotenv

load_dotenv()

# Server configuration.
serverConfig = {
    "name": os.getenv("SERVER_NAME"),
    "ip": os.getenv("HOST"),
    "port": os.getenv("PORT")
}

# TODO: Create socket.
try:
    server = socket.socket()
    TM.PrintTry(True, "Scoket created successfully.")
except:
    TM.PrintTry(False, "Error: Unable to create socket.")
    exit()

# TODO: Bind the socket using the serverConfig.
bindingConfig = (serverConfig["ip"], int(serverConfig["port"]))
try:
    server.bind(bindingConfig)
    TM.PrintTry(True, f"Success: Server binded to {bindingConfig}")
except:
    print(bindingConfig)
    TM.PrintTry(False, "Error: Unable to bind socket.")
    exit()

# TODO: Config the max no of connections it can accept and start listening.
noOfConnections = 5
try:
    server.listen(noOfConnections)
    TM.PrintTry(True, f"Success: Server is in listening mode with max connections: {noOfConnections}")
except:
    TM.PrintTry(False, "Error: Unable to start listening.")
    exit()

'''
    TODO: Run a loop that will stop when we interupt it or an error occured, inside the loop:
            1. Accept the new connection
            2. Send the public key to the client
            2. Send connection successful message with signature
            3. Ask for his name, send message with signature
            4. Receive his name
            5. Respond with welcome message and signature.
'''
while True:
    TM.PrintMessage("Waiting for an incomming connection.")

    # Accept the incomming connection.
    client, address = server.accept()
    TM.PrintMessage(f"Incomming connection from {address}")
    TM.PrintMessage(f"Connection accepted from {address}")

    publicKey, privateKey = Sign.generateKeyPair()
    encodedPublicKey = publicKey.export_key(format='PEM').encode()

    # TODO: Send the public key to the client
    length = len(encodedPublicKey).to_bytes(4, byteorder='big')
    client.send(length)
    client.send(encodedPublicKey)

    # Send connection successful response.
    message = "Successfully connected to server."
    encodedMessageSignature = Sign.generateSignature(message, privateKey)

    length = len(message.encode()).to_bytes(4, byteorder='big')
    client.send(length)
    client.send(message.encode())

    length = len(encodedMessageSignature).to_bytes(4, byteorder='big')
    client.send(length)
    client.send(encodedMessageSignature)

    # Ask for name.
    message = "Please provide you name."
    encodedMessageSignature = Sign.generateSignature(message, privateKey)

    length = len(message.encode()).to_bytes(4, byteorder='big')
    client.send(length)
    client.send(message.encode())

    length = len(encodedMessageSignature).to_bytes(4, byteorder='big')
    client.send(length)
    client.send(encodedMessageSignature)

    # Accept the name.
    receivedLength = client.recv(4)
    length = int.from_bytes(receivedLength, byteorder='big')
    encodedName = client.recv(length)

    # Send welcome message.
    message = f'{encodedName.decode()}, Welcome to {serverConfig["name"]}\'s server.'
    encodedMessageSignature = Sign.generateSignature(message, privateKey)

    length = len(message.encode()).to_bytes(4, byteorder='big')
    client.send(length)
    client.send(message.encode())

    length = len(encodedMessageSignature).to_bytes(4, byteorder='big')
    client.send(length)
    client.send(encodedMessageSignature)

    # Terminate the connection.
    client.close()
    TM.PrintMessage(f"Connection terminated from {address}")
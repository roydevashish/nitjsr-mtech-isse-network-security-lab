import socket
import TerminalMessage as TM
import HMAC as H
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
            2. Send connection successful message with digest
            3. Ask for his name, send message with digest
            4. Receive his name with digest
            5. Respond with welcome message and digest.
'''
while True:
    TM.PrintMessage("Waiting for an incomming connection.")

    # Accept the incomming connection.
    client, address = server.accept()
    TM.PrintMessage(f"Incomming connection from {address}")
    TM.PrintMessage(f"Connection accepted from {address}")

    # Send connection successful response.
    connectionSuccessfulMessage = "Successfully connected to server."
    encodedConnectionSuccessfulMessage, messageDigest = H.generate(connectionSuccessfulMessage)
    encodedMessageDigest = messageDigest.encode()

    length = len(encodedConnectionSuccessfulMessage).to_bytes(4, byteorder='big')
    client.send(length)
    client.send(encodedConnectionSuccessfulMessage)

    length = len(encodedMessageDigest).to_bytes(4, byteorder='big')
    client.send(length)
    client.send(encodedMessageDigest)

    # Ask for name.
    message = "Please provide you name."
    encodedMessage, messageDigest = H.generate(message)
    encodedMessageDigest = messageDigest.encode()

    length = len(encodedMessage).to_bytes(4, byteorder='big')
    client.send(length)
    client.send(encodedMessage)

    length = len(encodedMessageDigest).to_bytes(4, byteorder='big')
    client.send(length)
    client.send(encodedMessageDigest)

    # Accept the name.
    receivedLength = client.recv(4)
    length = int.from_bytes(receivedLength, byteorder='big')
    encodedName = client.recv(length)

    receivedLength = client.recv(4)
    length = int.from_bytes(receivedLength, byteorder='big')
    encodedNameDigest = client.recv(length)

    if(H.verify(encodedName, encodedNameDigest.decode())):
        # TODO: need to do something.
        # Send welcome message.
        welcomeMessage = f'{encodedName.decode()}, Welcome to {serverConfig["name"]}\'s server.'
        encodedWelcomeMessage, welcomeMessageDigest = H.generate(welcomeMessage)
        encodedWelcomeMessageDigest = welcomeMessageDigest.encode()

        length = len(encodedWelcomeMessage).to_bytes(4, byteorder='big')
        client.send(length)
        client.send(encodedWelcomeMessage)

        length = len(encodedWelcomeMessageDigest).to_bytes(4, byteorder='big')
        client.send(length)
        client.send(encodedWelcomeMessageDigest)
    else:
        # TODO: need to improve it.
        TM.PrintMessage("Error: This response is tampered.")
        exit()

    # Terminate the connection.
    client.close()
    TM.PrintMessage(f"Connection terminated from {address}")
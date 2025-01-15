import socket
import TerminalMessage as TM
from Encryption import aes

# Server Configuration
serverConfig = {
    "name": "NITJSR Network Security Lab",
    "ip": "localhost",
    "port": 8080
}

# TODO: Create socket.
try:
    server = socket.socket()
    TM.PrintTry(True, "Scoket created successfully.")
except:
    TM.PrintTry(False, "Error: Unable to create socket.")
    exit()

# TODO: Bind the socket using the serverConfig.
bindingConfig = (serverConfig["ip"], serverConfig["port"])
try:
    server.bind(bindingConfig)
    TM.PrintTry(True, f"Success: Server binded to {bindingConfig}")
except:
    TM.PrintTry(False, "Error: Unable to bind socket.")
    exit()

# TODO: Config the max no of connections it can accept and start listening
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
            2. Send a connection successfull message and 
            3. Ask for his name and respond with "Welcome {name}"
'''
while True:
    TM.PrintMessage("Waiting for an incomming connection.")

    # Accept the incomming connection.
    client, address = server.accept()
    TM.PrintMessage(f"Incomming connection from {address}")
    TM.PrintMessage(f"Connection accepted from {address}")

    # TODO: Create object for AES.
    AES = aes()

    # TODO: Encrypt the message.
    connectionSuccessfullMessage = "Success: Connected to server."
    encryptedConnectionSuccessfullMessage = AES.encrypt(connectionSuccessfullMessage)

    # Send connection successful response.    
    client.send(encryptedConnectionSuccessfullMessage)

    # TODO: Encrypt the message.
    message = "Please provide you name."
    encryptedMessage = AES.encrypt(message)

    # Ask for name.
    client.send(encryptedMessage)
    
    # Accept the name.
    name = client.recv(1024)

    # TODO: Decrypt the name.
    decryptedName = AES.decrypt(name)

    # Encrypt the welcome message.
    welcomeMessage = f'{decryptedName}, Welcome to {serverConfig["name"]}\'s server.'
    encryptedWelcomeMessage = AES.encrypt(welcomeMessage)

    # Send welcome message.
    client.send(encryptedWelcomeMessage)
    
    # Terminate the connection.
    client.close()
    TM.PrintMessage(f"Connection terminated from {address}")
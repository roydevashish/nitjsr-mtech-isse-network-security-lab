import socket
import TerminalMessage as TM
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Server configuration.
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
            2. Send connection successful message
            3. Generate RSA keys
            4. Send public key to client
            5. Ask for his name and respond with "Welcome {name}"
'''
while True:
    TM.PrintMessage("Waiting for an incomming connection.")

    # Accept the incomming connection.
    client, address = server.accept()
    TM.PrintMessage(f"Incomming connection from {address}")
    TM.PrintMessage(f"Connection accepted from {address}")

    # Send connection successful response.    
    connectionSuccessfulMessage = "Success: Connected to server.".encode()
    client.send(connectionSuccessfulMessage)

    # TODO: Generate RSA keys.
    key = RSA.generate(1024)
    privateKey = key
    publicKey = key.publickey()
    rawPublicKey = publicKey.exportKey()
    cipher = PKCS1_OAEP.new(privateKey)

    # TODO: Send public key to the client.
    client.send(rawPublicKey)   

    # Ask for name.
    message = "Please provide you name.".encode()
    client.send(message)
    
    # Accept the name.
    name = client.recv(1024)

    # TODO: Decrypt the name.
    decryptedName = cipher.decrypt(name).decode()

    # Send welcome message.
    welcomeMessage = f'{decryptedName}, Welcome to {serverConfig["name"]}\'s server.'.encode()
    client.send(welcomeMessage)
    
    # Terminate the connection.
    client.close()
    TM.PrintMessage(f"Connection terminated from {address}")
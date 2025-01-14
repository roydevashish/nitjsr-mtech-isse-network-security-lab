import socket
import TerminalMessage as TM

# TODO: Create Socket.
client = socket.socket()

# Server configuration
config = {
    "ip": "localhost",
    "port": 8080
}
serverConfig = (config["ip"], config["port"])

# TODO: Connect to server.
try:
    client.connect(serverConfig)
    # TODO: Receive the connection successfull message.
    TM.PrintTry(True, client.recv(1024).decode())
except:
    TM.PrintTry(False, "Unable to connect to server.")
    exit()

# TODO: Receive the ask name message.
TM.PrintMessage(client.recv(1024).decode())

# TODO: Send name to the server.
TM.PrintMessage("Your Name Please: ")
name = input()
client.send(name.encode())

# TODO: Receive the welcome message.
TM.PrintMessage(client.recv(1024).decode())

# TODO: Terminate the connection.
client.close()
from socket import *
import json

serverName = 'localhost'
serverPort = 5115
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    clientNumber = int(input("Input number between 1 and 100.\n"))
    clientName = input("Input your name.\n")
    data = {"name": clientName, "number": clientNumber}
    jsonData = json.dumps(data).encode()
    clientSocket.send(jsonData)
    response = clientSocket.recv(1024).decode()
    if (response == "User requests fulfilled.." or response == "Server Closed!!"):
        print("Connection Closed")
        clientSocket.close()
        break
    parsedResponse = json.loads(response)
    print(parsedResponse)
    print("Client Name: ", clientName, " | Server Name: ", parsedResponse["ServerName"],
          " | Server Number: ", parsedResponse["ServerNumber"])

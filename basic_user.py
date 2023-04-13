from socket import *
import json

serverName = 'localhost'
serverPort = 5115
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

clientNumber = int(input("Input number between 1 and 100.\n"))
clientName = input("Input your name.\n")
data = {"name": clientName, "number": clientNumber}
jsonData = json.dumps(data).encode()
clientSocket.send(jsonData)
if clientNumber > 100 or clientNumber < 1:
    clientSocket.close()
else:
    response = clientSocket.recv(1024).decode()
    parsedResponse = json.loads(response)
    print(parsedResponse)
    print("Client Name: ", clientName, " | Server Name: ", parsedResponse["server_name"],
          " | Server Number: ", parsedResponse["server_number"])
    clientSocket.close()

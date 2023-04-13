from socket import *
import json
import random

SERVER_NAME = "Wassim Server"
LISTNER_PORT = 5115

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', LISTNER_PORT))

while True:
    server_socket.listen()

    client = server_socket.accept()[0]
    client_data = client.recv(1024).decode()
    parsed_data = json.loads(client_data)
    if parsed_data["number"] > 100 or parsed_data["number"] < 1:
        break
    print(f'Client Name: {parsed_data["name"]} - Server Name: {SERVER_NAME}')
    server_number = random.randint(1, 100)

    print(
        f'Client Number: {parsed_data["number"]} - Server Number: {server_number} - Sum: {parsed_data["number"] + server_number}')

    summ = server_number + parsed_data["number"]

    client.send(json.dumps({"server_number": server_number,
                            "server_name": SERVER_NAME}).encode())

client.close()

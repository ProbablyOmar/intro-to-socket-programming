from socket import *
import json
import random

SERVER_NAME = "Wassim Server"
LISTNER_PORT = 5115

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', LISTNER_PORT))

server_socket.listen()

client = server_socket.accept()[0]
client_data = client.recv(1024).decode()
parsed_data = json.loads(client_data)
print(parsed_data)
server_number = random.randint(1, 100)

summ = server_number + parsed_data["number"]

client.send(json.dumps({"Sum": summ, "Sever Name": SERVER_NAME}).encode())
client.close()

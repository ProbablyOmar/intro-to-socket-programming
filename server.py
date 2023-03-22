from socket import *
import threading
import sys
import time
import random
import json

QUIT = False

SERVERNAME = 'Wassim Server'
LISTENERPORT = 5115


class ClientThread(threading.Thread):

    def __init__(self, client_sock):
        # Creating a new thread for client and passing it the client socket
        threading.Thread.__init__(self)
        self.client = client_sock

    def run(self):
        global QUIT
        done = False

        while not done:
            request = self.readline()
            clientNumber = int(request["number"])
            # User can close server by sending a number out of range(1 - 100)
            if (clientNumber > 100 or clientNumber < 1):
                self.sendResponse("Server Closed!!")
                print("Server Closed!!")
                done = True
                QUIT = True
            elif ('done' == request):
                self.sendResponse("User requests fulfilled..")
                done = True
            else:
                response = json.dumps(self.sum_(request))
                self.sendResponse(response)

        self.client.close()

    def readline(self):
        clientData = self.client.recv(1024).decode()
        parsedData = json.loads(clientData)
        print(parsedData)
        return parsedData

    def sum_(self, data):
        global QUIT
        clientName = data["name"]
        clientNumber = int(data["number"])

        if clientNumber > 100 or clientNumber < 1:
            self.writeline('Connection Closed!'.encode())
            QUIT = True
            return

        serverNumber = random.randint(1, 100)
        responseSum = serverNumber + clientNumber
        print(
            f'Client Name: {clientName} \n Server Number: {serverNumber} \n Client Number: {clientNumber} \n Sum: {responseSum}\n')
        return {"ServerName": SERVERNAME, "ServerNumber": serverNumber}

    def sendResponse(self, response):
        self.client.send(response.encode())


class Server:

    def __init__(self):
        self.listenerSocket = None
        self.thread_list = []

    def run(self):
        all_good = False
        try_count = 0
        while not all_good:
            if 3 < try_count:
                print("Could not bind to port - Port might be used..")
                sys.exit(1)
            try:
                self.listenerSocket = socket(AF_INET, SOCK_STREAM)
                self.listenerSocket.bind(('', LISTENERPORT))
                self.listenerSocket.listen(5)
                all_good = True
            except error:
                print("Socket connection error... Waiting 10 seconds to retry.")
                del self.listenerSocket
                time.sleep(10)
                try_count += 1

        print("Server is listening for incoming connections.")
        print("Try to connect through the command line, with:")
        print(f'telnet localhost {LISTENERPORT}')
        print("and then type whatever you want.")
        print()
        print("typing 'bye' finishes the thread, but not the server ",)
        print("(eg. you can quit telnet, run it again and get a different ")
        print("thread name")
        print("typing 'quit' finishes the server\n\n\n\n")
        try:
            while not QUIT:
                try:
                    self.listenerSocket.settimeout(0.5)
                    print("Listening...")
                    client = self.listenerSocket.accept()[0]
                except timeout:
                    time.sleep(1)
                    if QUIT:
                        print("Received quit command. Shutting down...")
                        break
                    continue
                newThread = ClientThread(client)
                print("Incoming Connection. Started thread ")
                print(newThread.name)
                self.thread_list.append(newThread)
                newThread.start()

                for thread in self.thread_list:
                    if not thread.is_alive():
                        self.thread_list.remove(thread)
                        thread.join()

        except KeyboardInterrupt:
            print('Ctrl+C pressed... Shutting Down')
        except Exception as err:
            print(f'Exception caught: {err} --- Closing...')

        for thread in self.thread_list:
            thread.join(1.0)
        self.listenerSocket.close()


if "__main__" == __name__:
    server = Server()
    server.run()

    print("Terminated")

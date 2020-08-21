import threading
import socket


host = '127.0.0.1' #Local
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicknames = []

#Broadcast function sends a message to connect clients
def broadCast(message):
    for client in clients:
        client.send(message)
#Handle client connection so recieve their message get it process it and broadcast
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadCast(message)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadCast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break
def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)} ")
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print(f'nickname of the client is {nickname}!')
        broadCast(f'{nickname} Joined the Chat!'.encode('ascii'))
        client.send("Connect to the server".encode('ascii'))

 #process people sending messages at the same time
        thread = threading.Thread(target = handle, args = (client,))
        thread.start()
print("Server is listening")
recieve()







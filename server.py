import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
names = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f"{name} left the chat".encode())
            names.remove(name)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NAME".encode())
        name = client.recv(1024).decode()

        names.append(name)
        clients.append(client)

        print(f"Name is {name}")
        broadcast(f"{name} joined the chat!".encode())
        client.send("Connected to server!".encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Server is running...")
receive()
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("127.0.0.1", 8080)

server_socket.bind(server_address)
server_socket.listen(1)

print("Server Active....Waiting for connection...")

connection, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

while True:
    data = connection.recv(1024)
    data=data.decode()

    if data=='exit':
        print("Client has disconnected.")
        break

    
    if data=="hello":
        print("Server Sent a Hai.")
        response = "hi there!"
        connection.send(response.encode())

connection.close()
server_socket.close()
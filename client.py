import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ("127.0.0.1", 8080)

client_socket.connect(server_address)
while True:
    message = input("Enter message to send (type 'exit' to quit): ")
    client_socket.send(message.encode())

    if message=='exit':
        break
        
    response = client_socket.recv(1024)
    response=response.decode()
    print(f"Server response: {response}")

client_socket.close()
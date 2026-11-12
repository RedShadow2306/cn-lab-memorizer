import socket
import threading

def handle_client(connection, client_address):
    print(f"Connection established with {client_address}")
    
    while True:
        data = connection.recv(1024)
        data = data.decode()
        
        if not data or data == 'exit':
            print(f"Client {client_address} has disconnected.")
            break
            
        print(f"Received from {client_address}: {data}")
        print("---------------------------------------------------")
        
        response = data
        connection.send(response.encode())
        
    connection.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("127.0.0.1", 8080)

server_socket.bind(server_address)
server_socket.listen(5)

print("Multi-user Chat Server Active....Waiting for connection...")

while True:
    connection, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
    client_thread.start()

server_socket.close()

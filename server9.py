import socket
import os
import threading

def handle_client(connection, client_address):
    print(f"Connection established with {client_address}")
    
    filename = connection.recv(1024).decode().strip()
    print(f"Requested filename: {filename}")
    
    pid = os.getpid()

    if os.path.exists(filename) and os.path.isfile(filename):
        with open(filename, "r") as f:
            file_contents = f.read()
        
        response = f"PID: {pid}\nFile Contents:\n{file_contents}"
        print(f"File found. Sent contents with PID {pid}.")
    else:
        response = f"PID: {pid}\nFile not found"
        print(f"File not found. Sent error message with PID {pid}.")

    connection.send(response.encode())
    connection.close()
    print("---------------------------------------------------")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("127.0.0.1", 9002)

server_socket.bind(server_address)
server_socket.listen(5)

print("File Server Active....Waiting for connection...")

while True:
    connection, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
    client_thread.start()

server_socket.close()

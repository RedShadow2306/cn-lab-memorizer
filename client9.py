import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("127.0.0.1", 9002)

client_socket.connect(server_address)

filename = input("Enter the filename to request: ")
client_socket.send(filename.encode())

response = client_socket.recv(4096)
response = response.decode()

print("---------------------------------------------------")
print(response)
print("---------------------------------------------------")

client_socket.close()

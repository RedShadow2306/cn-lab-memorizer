import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("127.0.0.1", 8080)

while True:
    Data = input("Enter a Sentence (type 'exit' to quit) : ")
    client_socket.sendto(Data.encode(), server_address)

    if Data == 'exit':
        break

    response, _ = client_socket.recvfrom(1024)
    response = response.decode()
    print(f"Server response: {response}")
client_socket.close()

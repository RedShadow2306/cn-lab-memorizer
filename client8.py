import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("127.0.0.1", 1234)

while True:
    message = input("Enter a message (type 'stop' to quit) : ")
    client_socket.sendto(message.encode(), server_address)

    if message == 'stop':
        print("Communication terminated.")
        break

    response, _ = client_socket.recvfrom(1024)
    response = response.decode()

    print(f"Server time: {response}")
    print("---------------------------------------------------")

client_socket.close()

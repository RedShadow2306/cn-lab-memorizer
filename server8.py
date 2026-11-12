import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("127.0.0.1", 1234)

server_socket.bind(server_address)
print("UDP Time Server Running...")

while True:
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode()

    print(f"Received message: {message} from {client_address}")
    print("---------------------------------------------------")

    if message == "stop":
        print("Client sent 'stop'. Terminating communication.")
        break

    current_time = time.localtime()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", current_time)

    server_socket.sendto(time_str.encode(), client_address)
    print(f"Sent time: {time_str}")
    print("---------------------------------------------------")

server_socket.close()
print("Server stopped.")

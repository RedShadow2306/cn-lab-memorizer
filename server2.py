import socket
import ast

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("127.0.0.1", 8080)

server_socket.bind(server_address)
server_socket.listen(1)
print("Server Active....Waiting for connection...")

connection, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

while True:
    data = connection.recv(1024)
    data = data.decode()

    if not data or data == 'exit':
        print("Client has disconnected.")
        break

    matrix = ast.literal_eval(data)
    for row in matrix:
        print(row)
    print("---------------------------------------------------")

    is_diagonal = True
    is_lower = True
    is_upper = True

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i > j and matrix[i][j] != 0:
                is_upper = False
            if i < j and matrix[i][j] != 0:
                is_lower = False
            if i != j and matrix[i][j] != 0:
                is_diagonal = False

    if is_diagonal:
        result = "Matrix Type = Diagonal Matrix!!!....."
    elif is_upper:
        result = "Matrix Type = UpperTriangular Matrix!!!....."
    elif is_lower:
        result = "Matrix Type = LowerTriangular Matrix!!!....."
    else:
        result = "Matrix Type = RegularMatrix!!!....."

    connection.send(result.encode())
connection.close()
server_socket.close()

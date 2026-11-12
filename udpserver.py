import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("127.0.0.1", 8080)

server_socket.bind(server_address)
print("UDP Server Running...")

abbreviations = {
    "tbh": "to be honest",
    "idc": "I don't care",
    "ig": "I guess",
    "tbf": "to be fair",
    "atm": "at the moment",
    "irl": "in real life",
    "lol": "laughing out loud",
    "asap": "as soon as possible",
    "omg": "oh my God",
    "ttyl": "talk to you later",
    "idk": "I don't know",
    "nvm": "never mind"
}

def translate(sentence):
    words = sentence.split()
    translated_words = []
    for word in words:
        lower_word = word.lower()
        if lower_word in abbreviations:
            translated_words.append(abbreviations[lower_word])
        else:
            translated_words.append(word)
    return " ".join(translated_words)

while True:
    data, client_address = server_socket.recvfrom(1024)
    sentence = data.decode()

    if sentence == "exit":
        print("Client disconnected.")
        break

    print(f"Received sentence: {sentence}")
    print("---------------------------------------------------")

    result = translate(sentence)
    server_socket.sendto(result.encode(), client_address)
    print("Translated message sent.")
    print("---------------------------------------------------")

server_socket.close()
print("Server stopped.")

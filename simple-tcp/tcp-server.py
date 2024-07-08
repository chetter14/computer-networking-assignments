from socket import *

server_port = 12_000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print('Server is ready to receive')

while True:
    connection_socket, client_address = server_socket.accept()
    sentence = connection_socket.recv(1024).decode()
    modified_sentence = sentence.upper()
    connection_socket.send(modified_sentence.encode())
    connection_socket.close()

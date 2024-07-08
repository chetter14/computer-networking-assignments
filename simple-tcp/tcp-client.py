from socket import *

server_name = 'serverName'
server_port = 12_000
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

sentence = input('Type a lowercase sentence:')
client_socket.send(sentence.encode())
modified_sentence = client_socket.recv(2048)

print('From server - ', modified_sentence.decode())
client_socket.close()
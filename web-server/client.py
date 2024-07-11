from socket import *
import sys

# goes from 1 because 'client.py' in 'python client.py ...' is at 0 index
server_host = sys.argv[1]
server_port = sys.argv[2]
filename = sys.argv[3]

# Create a Client class that can:
#   1) init a connection with server,
#   2) send a request to server
#   3) receive a reply
#   4) return the reply 


Bob_client_socket = socket(AF_INET, SOCK_STREAM)
Steve_client_socket = socket(AF_INET, SOCK_STREAM)

Bob_client_socket.connect((server_host, int(server_port)))
Steve_client_socket.connect((server_host, int(server_port)))
http_request = "GET /{filename} HTTP/1.1\r\nConnection: close\r\nHost: {server_host}\r\n\r\n ".format(filename=filename, server_host=server_host)

Bob_client_socket.send(http_request.encode())
Steve_client_socket.send(http_request.encode())

Bob_reply = Bob_client_socket.recv(2048).decode()
Steve_reply = Steve_client_socket.recv(2048).decode()

print('Bob! from server:\n' + Bob_reply + "\n")
print('Steve! from server:\n' + Steve_reply + "\n")

Bob_client_socket.close()
Steve_client_socket.close()

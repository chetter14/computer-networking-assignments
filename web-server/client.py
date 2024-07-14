from socket import *
import sys

# goes from 1 because 'client.py' in 'python client.py ...' is at 0 index
server_host = sys.argv[1]
server_port = sys.argv[2]
filename = sys.argv[3]


class ClientSocket:

    def __init__(self, server_host, server_port):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((server_host, server_port))
        self.server_host = server_host
        self.server_port = server_port  

    def send_get_request(self, filename):
        http_request = "GET /{filename} HTTP/1.1\r\nConnection: close\r\nHost: {server_host}\r\n\r\n ".format(filename=filename, server_host=self.server_host)
        self.client_socket.send(http_request.encode())

    def get_response(self):
        final_response = ""
        while True:
            cur_response = self.client_socket.recv(2048).decode()
            if not cur_response: break                      # if no response? ; taken from https://docs.python.org/3/library/socket.html#example 
            final_response = final_response + cur_response
        self.client_socket.close()
        return final_response


number_of_clients = 2
my_sockets = []

for i in range(number_of_clients):
    my_sockets.append(ClientSocket(server_host, int(server_port)))

for i in range(number_of_clients):
    my_sockets[i].send_get_request(filename)

for i in range(number_of_clients):
    response = my_sockets[i].get_response()
    print(str(i) + " client, the response - " + response)

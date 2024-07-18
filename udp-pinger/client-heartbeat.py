from socket import *
import sys
from datetime import datetime

server_host = sys.argv[1]
server_port = int(sys.argv[2])

client_socket = socket(AF_INET, SOCK_DGRAM)

for i in range(1, 11):
    print(datetime.now())
    message = "{sequence_number} {time}".format(sequence_number=i, time=datetime.now())
    client_socket.sendto(message.encode(), (server_host, server_port))

from socket import *
import sys
from datetime import datetime

server_host = sys.argv[1]
server_port = sys.argv[2]

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)     # 1 sec

message = "ping"

for i in range(10):
    send_time = datetime.now()
    client_socket.sendto(message.encode(), (server_host, int(server_port)))
    try:
        reply, server_address = client_socket.recvfrom(2048)
        receive_time = datetime.now()
        print("From server - " + reply.decode())
        
        delta_time = receive_time - send_time
        print("RTT - " + str(delta_time.total_seconds()))
    except timeout:
        print("Request timed out")

    print("")
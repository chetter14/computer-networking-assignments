from socket import *
import sys
from datetime import datetime

server_host = sys.argv[1]
server_port = sys.argv[2]

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)     # 1 sec

for i in range(1, 11):
    send_time = datetime.now()
    message = "ping {number} {time}".format(number=i, time=send_time)
    client_socket.sendto(message.encode(), (server_host, int(server_port)))
    try:
        reply, server_address = client_socket.recvfrom(2048)
        print("From server - {reply}".format(reply=reply.decode()))
        receive_time = datetime.now()
        delta_time = receive_time - send_time
        print("RTT (h:m:s.mcs) - {rtt}".format(rtt=delta_time))
    except timeout:
        print("Request timed out")

    print("")
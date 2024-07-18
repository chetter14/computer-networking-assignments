from socket import *
import sys
from datetime import datetime
import time
import random

server_host = sys.argv[1]
server_port = int(sys.argv[2])

client_socket = socket(AF_INET, SOCK_DGRAM)

for i in range(1, 11):
    sleep_seconds = random.randint(0, 7)
    print("Sleep for {time}s".format(time=sleep_seconds))
    time.sleep(sleep_seconds)

    current_time = datetime.now()
    print("{current_time}\n".format(current_time=current_time))
    message = "{sequence_number} {time}".format(sequence_number=i, time=current_time)
    client_socket.sendto(message.encode(), (server_host, server_port))

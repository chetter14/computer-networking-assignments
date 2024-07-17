from socket import *
import sys
from datetime import datetime

server_host = sys.argv[1]
server_port = sys.argv[2]

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)     # 1 sec

# in secs
min_rtt = 10.0
max_rtt = 0.0
total_rtt_sum = 0.0
rtt_number = 0

for i in range(1, 11):
    send_time = datetime.now()
    message = "ping {number} {time}".format(number=i, time=send_time)
    client_socket.sendto(message.encode(), (server_host, int(server_port)))

    try:
        reply, server_address = client_socket.recvfrom(2048)
        print("From server - {reply}".format(reply=reply.decode()))

        receive_time = datetime.now()
        delta_time = receive_time - send_time
        rtt = delta_time.seconds + delta_time.microseconds * 1e-6
        print("RTT - {rtt}s".format(rtt=rtt))

        if (rtt < min_rtt): min_rtt = rtt
        if (rtt > max_rtt): max_rtt = rtt

        total_rtt_sum = total_rtt_sum + rtt
        rtt_number = rtt_number + 1

    except timeout:
        print("Request timed out")

    print("")

print("RTT: min - {min}s, max - {max}s, average - {average}s".format(min=min_rtt, max=max_rtt, average=total_rtt_sum/rtt_number))
print("Packet loss - {loss}%".format(loss=(10.0 - rtt_number)/10.0 * 100.0))
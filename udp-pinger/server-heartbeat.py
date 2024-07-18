from socket import * 
from datetime import datetime

# Create a UDP socket  
# Notice the use of SOCK_DGRAM for UDP packets 
serverSocket = socket(AF_INET, SOCK_DGRAM) 
# Assign IP address and port number to socket 
serverSocket.bind(('', 6789)) 
serverSocket.settimeout(5)      # 5 sec

while True: 
    try:
        message, address = serverSocket.recvfrom(1024) 
        receive_time = datetime.now()
        print("From client:\n\t{message}".format(message=message.decode()))

        # parse the client time 
        client_message = message.split(' ')
        client_time_string = client_message[1] + " " + client_message[2]
        client_time = datetime.strptime(client_time_string, "%Y-%m-%d %H:%M:%S.%f")

        # calculate the difference
        delta_time = receive_time - client_time
        print("Delta time - {delta}\n".format(delta=delta_time))

    except timeout:
        print("The client application was closed.\n")
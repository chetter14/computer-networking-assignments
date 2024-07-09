from socket import *
from threading import Thread, Lock

import sys # In order to terminate the program 

server_socket = socket(AF_INET, SOCK_STREAM)
server_port = 6789
server_socket.bind(('', server_port))

max_clients_number = 3
server_socket.listen(max_clients_number)

mutex = Lock()
current_client_number = 0

print("Server is ready to receive messages!")

def connection_handling_function():

    global current_client_number

    try:
        mutex.acquire()
        # print("Added 1 to current_client_number")
        current_client_number = current_client_number + 1
        print("\nConnected to the " + str(current_client_number) + " client!")
        mutex.release()

        message = connection_socket.recv(2048).decode()

        # Read an HTML file
        filename = message.split()[1]
        f = open(filename[1:])
        output_data = f.readlines()

        print("Read the file!")

        # Send HTTP headers
        status_line = "HTTP/1.1 200 OK\r\n"
        connection_socket.send(status_line.encode())
        connection_header = "Connection: close\r\n"
        connection_socket.send(connection_header.encode())
        content_type_header = "Content-type: text/html\r\n"
        connection_socket.send(content_type_header.encode())

        connection_socket.send("\r\n".encode())

        print("Sent HTTP headers!")

        # Send the content of the requested file
        for i in range(0, len(output_data)):
            connection_socket.send(output_data[i].encode())
        connection_socket.close()

        print("Sent the HTML file!\n")

    except IOError:
        print("IO error!")
        status_line = "HTTP/1.1 404 Not Found\r\n"
        connection_socket.send(status_line.encode())

        connection_header = "Connection: close\r\n"
        connection_socket.send(connection_header.encode())
        connection_socket.send("\r\n".encode())

        entity = "404 Not Found"
        connection_socket.send(entity.encode())
        connection_socket.close()
        
        print("Closed the connection!\n")

    mutex.acquire()
    # print("Subtracted 1 from current_client_number")
    current_client_number = current_client_number - 1
    mutex.release()


while True:
    connection_socket, client_address = server_socket.accept()
    client_thread = Thread(target=connection_handling_function)
    client_thread.start()
    # client_thread.join()


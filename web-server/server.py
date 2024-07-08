from socket import *

import sys # In order to terminate the program 

server_socket = socket(AF_INET, SOCK_STREAM)
server_port = 6789
server_socket.bind(('', server_port))
server_socket.listen(1)
print("Server is ready to receive messages!")

while True:
    print('Ready to serve')
    connection_socket, client_address = server_socket.accept()

    try:
        print("Connected!")
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

        print("Sent the HTML file!")

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
        
        print("Closed the connection!")

    server_socket.close()

    sys.exit()
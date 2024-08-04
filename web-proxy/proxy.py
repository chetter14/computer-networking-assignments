from socket import * 
import sys 
    
# Create a server socket, bind it to a port and start listening 
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('', 8888))
tcpSerSock.listen(1)

pages_cache = {}

while 1: 
    # Start receiving data from the client 
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    message = tcpCliSock.recv(2048).decode()
    while not message:
        message = tcpCliSock.recv(2048).decode()
    print("Received message:\n{message}".format(message=message))

    # Extract the filename from the given message 
    full_path = message.split()[1][1:]           # with no '/' before the name of the file
    print("Full path - {full_path}".format(full_path=full_path))

     # Check whether such a file exists in the cache
    if full_path in pages_cache:                            # if yes, then cache hit and send to the client
        tcpCliSock.send(pages_cache[full_path].encode())
        print('Read from cache\n')
    else:
        # Get the host and the requested file
        host, slash, file = full_path.partition("/")

        # Create a socket on the proxyserver    
        proxy_client_socket = socket(AF_INET, SOCK_STREAM)
        hostn = host.replace("www.","",1)
        print("Hostname - {host}".format(host=hostn))
                                                 
        try:     
            # Connect to the socket to port 80     
            proxy_client_socket.connect((hostn, 80))
            print("Successfully connected to host")

            # Redirect the request to the server
            http_request = "GET /{file} HTTP/1.0\r\nHost: {host}\r\n\r\n ".format(file=file, host=hostn)
            proxy_client_socket.send(http_request.encode())
            print("Sent the request - " + http_request)

            # Read the response into buffer
            final_response = ""
            while True:
                cur_response = proxy_client_socket.recv(2048).decode()
                if not cur_response: break
                final_response = final_response + cur_response

            print("Received the data from the server:\n" + final_response)

            # Store the response in the cache   
            pages_cache[full_path] = final_response
            print("Stored the data in the cache")

            # Send the response to the client socket     
            tcpCliSock.send(final_response.encode())

        except:     
            print("Error! Something went wrong during the interaction with the server!\n\n")     
                          
    # Close the client
    tcpCliSock.close()  
    
tcpSerSock.close()
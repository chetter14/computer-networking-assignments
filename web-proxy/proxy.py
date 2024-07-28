from socket import * 
import sys 

# if len(sys.argv) <= 1: 
#     print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server') 
#     sys.exit(2) 
      
# Create a server socket, bind it to a port and start listening 
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(('', 8888))
tcpSerSock.listen(1)  

while 1: 
    # Start receiving data from the client 
    print('Ready to serve...') 
    tcpCliSock, addr = tcpSerSock.accept() 
    print('Received a connection from:', addr) 
    message = tcpCliSock.recv(2048).decode()
    print("Received message:\n {message}".format(message=message))

    # Extract the filename from the given message 
    filename = message.split()[1][1:]           # with no '/' before the name of the file 
    print("Filename - {filename}".format(filename=filename)) 
    
    try: 
        # Check whether the file exist in the cache   
        f = open(filename, "r")
        outputdata = f.readlines() 
        f.close()

        # ProxyServer finds a cache hit and generates a response message   
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())              
        tcpCliSock.send("Content-Type:text/html\r\n".encode())   
        tcpCliSock.send("\r\n".encode())

        # Send the content of the file
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i])
        tcpCliSock.send("\r\n".encode())

        print('Read from cache\n')

    # Error handling for file not found in cache  
    except IOError:   

        # Create a socket on the proxyserver    
        proxy_client_socket = socket(AF_INET, SOCK_STREAM)
        hostn = filename.replace("www.","",1)
        print("Hostname - {host}".format(host=hostn))
                                                 
        try:     
            # Connect to the socket to port 80     
            proxy_client_socket.connect((hostn, 80)) 
            print("Successfully connected to host")

            # Redirect the request to the server
            fileobj = proxy_client_socket.makefile('r', 0)   
            fileobj.write("GET "+"http://" + filename + " HTTP/1.0\r\n\r\n")   

            data = fileobj.read(2048)

            # http_request = "GET http://{uri} HTTP/1.0\r\n\r\n ".format(uri=filename)
            # proxy_client_socket.send(http_request.encode())
            # print("Sent the request - " + http_request)

            # # Read the response into buffer     
            # final_response = ""
            # while True:
            #     cur_response = proxy_client_socket.recv(2048).decode()
            #     if not cur_response: break
            #     final_response = final_response + cur_response

            # print("Received the data from the server:\n" + final_response)

            # Create a new file in the cache for the requested file.      
            localFile = open(filename, "wb")
            localFile.write(data)
            localFile.close()

            print("Printed the data to the file")

            # Send the response in the buffer to client socket and the corresponding file in the cache     
            tcpCliSock.send(data)      

        except:     
            print("Illegal request")                                                
    
    # Close the client and the server sockets      
    tcpCliSock.close()  
    
tcpSerSock.close()
# Fill in start.   
# Fill in end. 
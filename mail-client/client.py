from socket import * 

# Choose a mail server (e.g. Google mail server) and call it mailserver 
mailserver = '209.85.233.108'
 
# Create socket called clientSocket and establish a TCP connection with mailserver 
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 587))

recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '220': 
    print('220 reply not received from server.') 
    
# Send HELO command and print server response. 
helloFrom = "gmail.com"
heloCommand = 'HELO {helloFrom}\r\n'.format(helloFrom=helloFrom) 
clientSocket.send(heloCommand.encode()) 
recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '250': 
    print('HELO: 250 reply not received from server.') 
    
# Send STARTTLS command for security issues         
# TLS 1.2 is not supported by Python 2.7
startTlsCommand = 'STARTTLS'
clientSocket.send(startTlsCommand.encode()) 
recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '220':   
    print('STARTTLS: 220 reply not received from server.') 

# Send MAIL FROM command and print server response. 
senderMail = "artemleshchukov02@gmail.com"
mailFromCommand = 'MAIL FROM: <{mail}>\r\n'.format(mail=senderMail)
clientSocket.send(mailFromCommand.encode()) 
recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '250': 
    print('MAIL FROM: 250 reply not received from server.') 

# Send RCPT TO command and print server response.
rcptMail = "artem-leshchukov@mail.ru"  
rcptToCommand = 'RCPT TO: <{mail}>\r\n'.format(mail=rcptMail)
clientSocket.send(rcptToCommand.encode()) 
recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '250': 
    print('RCPT TO: 250 reply not received from server.') 

# Send DATA command and print server response.  
dataCommand = 'DATA\r\n' 
clientSocket.send(dataCommand.encode()) 
recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '354': 
    print('DATA: 354 reply not received from server.') 

# Send message data that ends with a single period
messageCommand = "I love computer networks!\r\n.\r\n" 
clientSocket.send(messageCommand.encode())
recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '250': 
    print('MESSAGE: 250 reply not received from server.') 

# Send QUIT command and get server response. 
quitCommand = "QUIT\r\n" 
clientSocket.send(quitCommand.encode()) 
recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '221': 
    print('QUIT: 221 reply not received from server.') 
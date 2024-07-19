from socket import * 
msg = "\r\n I love computer networks!" 
endmsg = "\r\n.\r\n" 

# Choose a mail server (e.g. Google mail server) and call it mailserver 
mailserver = '77.88.21.249' # I use a Yandex mail server
 
# Create socket called clientSocket and establish a TCP connection with mailserver 
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 25))

recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '220': 
    print('220 reply not received from server.') 
    
# Send HELO command and print server response. 
heloCommand = 'HELO Alice\r\n' 
clientSocket.send(heloCommand.encode()) 
recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '250': 
    print('HELO: 250 reply not received from server.') 
    
# Send MAIL FROM command and print server response. 
mailFromCommand = 'MAIL FROM: <artemleshchukov02@gmail.com>\r\n' 
clientSocket.send(mailFromCommand.encode()) 
recv = clientSocket.recv(1024).decode() 
print(recv) 
if recv[:3] != '250': 
    print('MAIL FROM: 250 reply not received from server.') 

# Send RCPT TO command and print server response.  
rcptToCommand = 'RCPT TO: <chetter-14@yandex.ru>\r\n' 
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

# Send message data with "." on a single line
messageCommand = "Hey, it's me!\r\nHow are you doing?\r\n.\r\n" 
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
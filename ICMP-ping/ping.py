from socket import *
import os
import sys
import struct
import time
import select
import datetime
import binascii

ICMP_ECHO_REQUEST = 8

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    
    while count < countTo:
        thisVal = ord(string[count+1]) * 256 + ord(string[count])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)

    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        
        if whatReady[0] == []: # Timeout
            return "Request timed out."
        
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        #Fetch the ICMP header from the IP packet

        echo_reply = struct.unpack("qqibbHHhff", recPacket)
        # print(echo_reply)

        # in binary format we read from recPacket into 2 floats but we need 1 double
        icmp_header_index = 3
        double_struct = struct.pack("ff", echo_reply[icmp_header_index + 5], echo_reply[icmp_header_index + 6])
        time_in_packet = struct.unpack("d", double_struct)[0]
       
        delta = timeReceived - time_in_packet

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."
        else:
            return delta
        

def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum 
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(str(header + data))
    
    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.


def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details: http://sock-raw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF # Return the current process i

    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay


def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    
    pings_number = 10

    min_rtt = 10
    max_rtt = 0
    total_rtt_sum = 0
    rtt_number = 0
    packets_lost = 0

    # Send ping requests to a server separated by approximately one second
    for i in range(pings_number) :
        delay = doOnePing(dest, timeout)
        print("RTT - " + str(delay) + "s")

        if isinstance(delay, str):
            packets_lost = packets_lost + 1
        else:
            if delay < min_rtt:
                min_rtt = delay
            elif delay > max_rtt:
                max_rtt = delay
            total_rtt_sum = total_rtt_sum + delay
            rtt_number = rtt_number + 1

        time.sleep(1)# one second
    
    print("")
    print("Max RTT - " + str(max_rtt) + "s")
    print("Min RTT - " + str(min_rtt) + "s")
    print("Average RTT - " + str(total_rtt_sum / rtt_number) + "s")
    print("Packets lost - " + str(packets_lost / pings_number * 100) + "%")

    return delay


ping("vk.com")
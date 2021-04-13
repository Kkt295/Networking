
from socket import *
import os
import sys
import struct
import time
import select
import binascii
import statistics
# Should use stdev

ICMP_ECHO_REQUEST = 8

def checksum(string):
   csum = 0
   countTo = (len(string) // 2) * 2
   count = 0

   while count < countTo:
       thisVal = (string[count + 1]) * 256 + (string[count])
       csum += thisVal
       csum &= 0xffffffff
       count += 2

   if countTo < len(string):
       csum += (string[len(string) - 1])
       csum &= 0xffffffff

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
       if whatReady[0] == []:  # Timeout
           # print( "Request timed out.")
           return 0

       timeReceived = time.time()
       recPacket, addr = mySocket.recvfrom(1024)

       # Fill in start

       # Fetch the ICMP header from the IP packet -- cksum, sequence number, time to live (TTL), etc. see send one ping "packet for what to process"
       #recIpHeader = recPacket[0:20]
       recIpHeader = struct.unpack("!BBHHHBBHII", recPacket[0:20])
       recIcmpHeader = recPacket[20:28]
       recType, recCode, recChecksum, recID, recSequence = struct.unpack("bbHHh", recIcmpHeader)
       
       if (ID == recID):
            sizeOfData = struct.calcsize("d")
            recData = struct.unpack("d",recPacket[28:28 + sizeOfData])
            timeSent = recData[0]
            totalTime = (timeReceived - timeSent) * 1000

            # print ("Reply from " + str(destAddr) + ": bytes=" + str( 28 + sizeOfData ) + " time=" + str(totalTime)[0:10] + "ms TTL=" + str(recIpHeader[5]))

            return totalTime

       # Fill in end
       timeLeft = timeLeft - howLongInSelect
       if timeLeft <= 0:
            # print( "Request timed out.")
            return 0

def sendOnePing(mySocket, destAddr, ID):
   # Header is type (8), code (8), checksum (16), id (16), sequence (16)

   myChecksum = 0
   # Make a dummy header with a 0 checksum
   # struct -- Interpret strings as packed binary data
   header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
   data = struct.pack("d", time.time())
   # Calculate the checksum on the data and the dummy header.
   myChecksum = checksum(header + data)

   # Get the right checksum, and put in the header

   if sys.platform == 'darwin':
       # Convert 16-bit integers from host to network  byte order
       myChecksum = htons(myChecksum) & 0xffff
   else:
       myChecksum = htons(myChecksum)

   header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
   packet = header + data

   mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str

   # Both LISTS and TUPLES consist of a number of objects
   # which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
   icmp = getprotobyname("icmp")

   # SOCK_RAW is a powerful socket type. For more details:   http://sockraw.org/papers/sock_raw
   mySocket = socket(AF_INET, SOCK_RAW, icmp)

   myID = os.getpid() & 0xFFFF  # Return the current process i
   sendOnePing(mySocket, destAddr, myID)
   delay = receiveOnePing(mySocket, myID, timeout, destAddr)
   mySocket.close()
   return delay

def ping(host, timeout=1):
   # timeout=1 means: If one second goes by without a reply from the server,      # the client assumes that either the client's ping or the server's pong is lost
   dest = gethostbyname(host)
   #print("Pinging " + dest + " using Python:")
   #print("")
   # Calculate vars values and return them
   #  vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)),str(round(stdev(stdev_var), 2))]
   # Send ping requests to a server separated by approximately one second

   delays = []

   for i in range(0,4):
       delay = doOnePing(dest, timeout)
       delays.append(delay)

       time.sleep(1)  # one second

   packet_min = min(delays)
   packet_max = max(delays)
   packet_avg =statistics.mean(delays)
   stdev_var = statistics.pstdev(delays)
   #stdev_var = ((delays[0]-packet_avg) + (delays[1]-packet_avg) + (delays[2]-packet_avg) + (delays[3]-packet_avg))/4.0



   #print(str(packet_min))
   #print(str(packet_max))
   #print(str(packet_avg))
   #print(str(stdev_var))

   
   vars = [str(round(packet_min, 2)), str(round(packet_avg, 2)), str(round(packet_max, 2)), str(round(stdev_var, 2))]

   #vars = [packet_min,packet_avg,packet_max,stdev_var]
   return vars

#if __name__ == '__main__':
 #  ping("google.co.il")

ping("www.google.com")

from socket import *
import ssl


def smtp_client(port=1025, mailserver='127.0.0.1'):

   msg = "\r\n My message"
   endmsg = "\r\n.\r\n"

   # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope
   #mailserver = "smtp.gmail.com"
   #port = 587

   # Create socket called clientSocket and establish a TCP connection with mailserver and port
   clientSocket = socket(AF_INET, SOCK_STREAM)
   clientSocket.connect((mailserver, port))

   #recv = clientSocket.recv(1024).decode()
   #print(recv)
   #if recv[:3] != '220':
      #print('220 reply not received from server.')

   # Send HELO command and print server response.
   heloCommand = 'HELO Alice\r\n'
   clientSocket.send(heloCommand.encode())
   #recv1 = clientSocket.recv(1024).decode()
   #print(recv1)
   #if recv1[:3] != '250':
      #print('250 reply not received from server.')

   #Encrypting Connection
   #TlsCommand = 'STARTTLS\r\n'
   #clientSocket.send(TlsCommand.encode())
   #recv2 = clientSocket.recv(1024).decode()
   #print (recv2)
   #if recv2[:3] != '220':
      #print ('220 reply not received from server')

   # Encrypting Socket
   #ssl_clientSocket = socket.ssl(clientSocket)

   # Send MAIL FROM command and print server response.
   #sender = "<username@gmail.com>"
   #MailFrom = 'MAIL FROM: ' + sender + '\r\n'
   #clientSocket.send(MailFrom.encode())
   #recv3 = clientSocket.recv(1024)
   #print (recv3)
   #if recv3[:3] != '250':
      #print('250 reply not received from server.')

   # Send RCPT TO command and print server response.
   #recipient = "<username@gmail.com>"
   #rcptToCommand = 'RCPT TO: ' + recipient + '\r\n'
   #clientSocket.send(rcptToCommand.encode())
   #recv4 = clientSocket.recv(1024)
   #print (recv4)
   #if recv4[:3] != '250':
      #print('250 reply not received from server.')

   # Send DATA command and print server response.
   dataCommand = 'DATA\r\n'
   clientSocket.send(dataCommand.encode())
   recv5 = clientSocket.recv(1024)
   #print (recv5)
   #if recv5[:3] != '354':
      #print('354 reply not received from server.')

   # Send message data.
   clientSocket.send(msg.encode())

   # Message ends with a single period.
   clientSocket.send(endmsg.encode())
   recv6 = clientSocket.recv(1024)
   #print (recv6)
   #if recv6[:3] != '250':
      #print ('250 reply not received from server.')

   # Send QUIT command and get server response.
   quitCommand = 'QUIT\r\n'
   clientSocket.write(quitCommand.encode())
   #recv7 = ssl_clientSocket.recv(1024)
   #print (recv7)
   #if recv7[:3] != '221':
      #print ('221 reply not received from server.')


if __name__ == '__main__':
   smtp_client(1025, '127.0.0.1')

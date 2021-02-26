from socket import *


def smtp_client(port=1025, mailserver='127.0.0.1'):

   msg = "\r\n My message"
   endmsg = "\r\n.\r\n"

   # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope
   mailserver = "smtp.gmail.com"
   port = 587

   # Create socket called clientSocket and establish a TCP connection with mailserver and port
   clientSocket = socket.socket()
   clientSocket.connect((mailserver, port)).decode()

   recv = clientSocket.recv(1024).decode()
   #print(recv)
   if recv[:3] != '220':
      #print('220 reply not received from server.')

   # Send HELO command and print server response.
   heloCommand = 'HELO Alice\r\n'
   clientSocket.send(heloCommand.encode())
   recv1 = clientSocket.recv(1024).decode()
   #print(recv1)
   if recv1[:3] != '250':
      #print('250 reply not received from server.')

   #Encrypting Connection
   clientSocket.send('STARTTLS\r\n')
   recv2 = clientSocket.recv(1024).decode()
   #print (recv2)
   if recv2[:3] != '220':
      #print ('220 reply not received from server')

   # Encrypting Socket
   ssl_clientSocket = socket.ssl(clientSocket)

   # Send MAIL FROM command and print server response.
   sender = "<username@gmail.com>"
   MailFrom = 'MAIL FROM: ' + sender + '\r\n'
   ssl_clientSocket.write(MailFrom)
   recv3 = ssl_clientSocket.recv(1024)
   #print (recv2)
   if recv3[:3] != '250':
      #print('250 reply not received from server.')

   # Send RCPT TO command and print server response.
   recipient = "<username@gmail.com>"
   rcptToCommand = 'RCPT TO: ' + recipient + '\r\n'
   ssl_clientSocket.write(rcptToCommand)
   recv4 = ssl_clientSocket.recv(1024)
   #print (recv3)
   if recv4[:3] != '250':
      #print('250 reply not received from server.')

   # Send DATA command and print server response.
   dataCommand = 'DATA\r\n'
   ssl_clientSocket.write(dataCommand)
   recv5 = ssl_clientSocket.recv(1024)
   #print (recv4)
   if recv5[:3] != '354':
      #print('354 reply not received from server.')

   # Send message data.
   ssl_clientSocket.write(msg)

   # Message ends with a single period.
   ssl_clientSocket.write(endmsg)
   recv6 = ssl_clientSocket.recv(1024)
   #print (recv5)
   if recv6[:3] != '250':
      #print ('250 reply not received from server.')

   # Send QUIT command and get server response.
   quitCommand = 'QUIT\r\n'
   ssl_clientSocket.write(quitCommand)
   recv7 = ssl_clientSocket.recv(1024)
   #print (recv6)
   if recv7[:3] != '221':
      #print ('221 reply not received from server.')


if __name__ == '__main__':
   smtp_client(1025, '127.0.0.1')

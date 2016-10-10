import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
host = raw_input("Enter Pi ip address: ")
port = 9999
counter = 0;
print "Connecting..."
s.connect((host, port))
print "Connection successful"
while True:
	#Wait for server to send dataReady message
	fileString = "dataRecv" + str(counter) + ".txt";
	f = open(fileString, 'wb')
	serverMessage = str(s.recv(64))
	if(serverMessage == "DataReady"):
		s.sendall("ack") #Send acknowledgment
		serverMessage = s.recv(64)
		while serverMessage:
			f.write(serverMessage)
			try:
				serverMessage = s.recv(64)
			except:
				break
		print "Server timeout, file ended"
		f.close()
		#Send OK to server that new file can be sent
		s.sendall("OK")
		counter += 1
s.close()


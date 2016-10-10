import socket

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.settimeout(10)
host = ''
port = 9999
s.bind((host, port))
s.listen(5)
print "Awaiting connection"
sc, address = s.accept()
print ("Client " + str(address) + " connected.")
while True:

	#filename = raw_input("Enter File to Send: ")
        f = open("fakeData.txt", 'rb')

	message = "DataReady"
	#Wait for client to send acknowldegment
	sc.send(message)

	# Wait for user to send acknowledgment
	while True:
		reply = str(sc.recv(64))
		if(reply == "ack"):
                        print "Ack received"
			bits = f.read(64)
			while(bits):
				sc.send(bits)
				bits = f.read(64)
			print "File Ended"
			break
	f.close()
        print "Outside whileLoop"
	#Wait for client to send OK to send new file
        if (str(sc.recv(64)) == "OK"):
                continue
	

s.close()


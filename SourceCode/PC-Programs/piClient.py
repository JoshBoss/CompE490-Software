import socket

host = '192.168.42.1'
port = 8890

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

while True:
	command = raw_input("Enter your command: ")
	if command == 'EXIT':
		# Send EXIT request to other end
		s.send(command)
		break
	elif command == 'KILL':
		# Send KILL command
		s.send(command)
		break
	s.sendall(command)
	reply = s.recv(1024)
	print (reply)

s.close()


import socket		#Import the socket module

import RPi.GPIO as GPIO	#Import GPIO module

#Setup pin 18 (BCM) as output
LEDPin = 18;
GPIO.setmode(GPIO.BCM);
GPIO.setup(LEDPin, GPIO.OUT);


s = socket.socket();	#Create a socket object

host = socket.gethostname(); #Get local machine name

port = 12345;		     #Reserve a port for this communication service

s.bind((host, port)); 	     # Bind to the port

s.listen(5);		     # Wait for connection

while True:
	c, addr = s.accept()	# Establish connection with client
	print "Got connection from", addr
	c.send("Raspberry Pi.\nEnter 1 to Turn LED on\nEnter 2 to Turn LED off")
	data = s.recv(1024); # Wait to receive data
	if(data == "1"):
		GPIO.output(LEDPin, 1);
	elif (data == "2"):
		GPIO.output(LEDPin, 0);



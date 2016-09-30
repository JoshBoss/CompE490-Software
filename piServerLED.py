import socket
import RPi.GPIO as GPIO

LEDPin = 18
LEDPinStatus = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEDPin, GPIO.OUT)
GPIO.setup(LEDPinStatus, GPIO.IN)

host = ''
port = 8890

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print ("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
            print(msg)
    print("Socket binding successful.")
    return s

def setupConnection():
    s.listen(1) #Will only allow 1 connection at a time.
    conn, address = s.accept()
    print ("Connected to: " + address[0] + ":" + str(address[1]))
    return (conn, address)

def PING():
    return "Pi pinged successfully"

def LEDON():
    GPIO.output(LEDPin, 1)
    return "LED now on"

def LEDOFF():
    GPIO.output(LEDPin, 0)
    return "LED now off"

def LEDSTATUS():
    return str("LED value is " + str(GPIO.input(LEDPinStatus)))

def dataTransfer(conn, address):
    # Loop that sends/receives data until told not to
    while True:
        data = str(conn.recv(1024)) #Buffer size of 1024 bits?
        if data == 'PING':
            reply = PING()
        elif data == 'LEDON':
            reply = LEDON()
        elif data == 'LEDOFF':
            reply = LEDOFF()
        elif data == 'LEDSTATUS':
            reply = LEDSTATUS()
        elif data == 'EXIT':
            print ("Client " + str(address) + " has left.")
            break
        elif data == 'KILL':
            print ("KILL command detected. Shutting down Pi server.")
            s.close()
            break
        else:
            reply = 'Unknown Command. Try Again'

        conn.sendall(reply)
        print("Reply sent.")
    conn.close()

s = setupServer()

while True:
    try:
        (conn, address) = setupConnection()
        dataTransfer(conn, address)
    except:
        break
GPIO.cleanup()

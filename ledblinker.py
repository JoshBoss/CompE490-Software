import RPi.GPIO as IO
import time

LEDPin = 18;
IO.setmode(IO.BCM)
IO.setup(LEDPin, IO.OUT)

for i in range(0, 100):
	IO.output(LEDPin, 1)
	time.sleep(0.05)
	IO.output(LEDPin, 0)
	time.sleep(0.05)


#Make sure to turn LED off before exiting
IO.output(LEDPin, 0)
IO.cleanup()

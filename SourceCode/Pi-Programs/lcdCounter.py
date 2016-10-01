import lcddriver
import time

LCD = lcddriver.lcd()

for i in range(0,10000):
	LCD.lcd_display_string(str(i), 1)
	time.sleep(0.035)
	LCD.lcd_clear()

LCD.lcd_clear()


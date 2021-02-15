try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("...error importing RPi.GPIO module")

from time import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT)

for i in range(10): #  ei taha while(True) loopi teha
	GPIO.output(38, 1)
	print("high")
	sleep(0.5)
	GPIO.output(38, 0)
	print("low")
	sleep(0.5)
GPIO.cleanup(40)

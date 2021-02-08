try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("...error importing RPi.GPIO module")

from time import sleep

GPIO.setmode(GPIO.BOARD)
pins=[36, 38]
GPIO.setup(pins, GPIO.OUT)

for i in range(2): #  ei taha while(True) loopi teha
	GPIO.output(36, 1)
	GPIO.output(38, 0)
	sleep(0.5)
	GPIO.output(36, 0)
	GPIO.output(38, 1)
	sleep(0.5)
GPIO.cleanup(pins)

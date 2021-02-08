try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("...error importing RPi.GPIO module")

from time import sleep

GPIO.setmode(GPIO.BOARD)
pins=[37,35,33,31,29,23,21,19]
GPIO.setup(pins, GPIO.IN)

activePins = []
inactivePins = pins.copy()
activePins.append(inactivePins.pop(0))
for i in range(2): #  ei taha while(True) loopi teha
	for i in range(len(pins)):
		GPIO.input(activePins, 1)
		GPIO.input(inactivePins, 0)
		activePins.append(inactivePins.pop(0))
		inactivePins.append(activePins.pop(0))
		sleep(0.1)
		print(activePins)
	for i in range(len(pins)):
		GPIO.input(activePins, 1)
		GPIO.input(inactivePins, 0)
		activePins.append(inactivePins.pop(-1))
		inactivePins.insert(0,activePins.pop(0))
		sleep(0.1)
		print(activePins)
GPIO.cleanup(pins)

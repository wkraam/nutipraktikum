#!/usr/bin/python3
try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("...error importing RPi.GPIO module")

from time import sleep

GPIO.setmode(GPIO.BOARD)
pins=[36, 38]
GPIO.setup(pins, GPIO.OUT)
sleepTime = 0.5
while True:
	GPIO.output(36, 1)
	GPIO.output(38, 0)
	sleep(sleepTime)
	GPIO.output(36, 0)
	GPIO.output(38, 1)
	sleep(sleepTime)
	print(sleepTime)
GPIO.cleanup(pins)

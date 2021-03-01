#!/usr/bin/python3
class Blinker:
	sleepTime = 0.5
	def __init__(self, sleepTime = 0.5):
		print("Blink initialized")
		self.sleepTime = sleepTime

	def setSleepTime(self, time):
		self.sleepTime = time

	def getSleepTime(self):
		print(self.sleepTime)
	def main(self):
		try:
			import RPi.GPIO as GPIO
		except RuntimeError:
			print("...error importing RPi.GPIO module")
		from time import sleep

		GPIO.setmode(GPIO.BOARD)
		pins=[36, 38]
		GPIO.setup(pins, GPIO.OUT)
		while True:
			GPIO.output(36, 1)
			GPIO.output(38, 0)
			sleep(self.sleepTime)
			GPIO.output(36, 0)
			GPIO.output(38, 1)
			sleep(self.sleepTime)
		print(getSleepTime())
	def stop(self):
		GPIO.cleanup(pins)

if __name__ == "__main__":
	Blinker = Blinker()
	Blinker.getSleepTime()
	Blinker.stop()


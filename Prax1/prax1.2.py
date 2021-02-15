'''
-----   7-segment led display   GPIO ühendused

	31
      29  33
 	23
      21  35
	19  37
'''


try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("...error importing RPi.GPIO module")

from time import sleep
import sys
import signal
from random import randint

#------------pinnide setup-----------
GPIO.setmode(GPIO.BOARD)
pins=[37,35,33,31,29,23,21,19]
GPIO.setup(pins, GPIO.OUT)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#-----------btn interrupt-----------
def signal_handler(sig, frame):
	GPIO.cleanup()
	GPIO.exit(0)

def bttn_callback(channel):
	global suund
	print("nupp")
	if suund == 1:
		suund = 2
	elif suund == 2:
		suund = 3
	elif suund == 3:
		suund = 1
	print(suund)

#-----------mis pin on mis numbril tähtis---------
def show1():
	GPIO.output(33, 0)
	GPIO.output(35, 0)

def show2():
	number = [31, 33, 23, 21, 19]
	GPIO.output(number, 0)

def show3():
	number = [31, 33, 23, 35, 19]
	GPIO.output(number, 0)

def show4():
	number = [29, 23, 33, 35]
	GPIO.output(number, 0)

def show5():
	number = [31, 29, 23, 35, 19]
	GPIO.output(number, 0)

def show6():
	number = [31, 29, 23, 35, 19, 21]
	GPIO.output(number, 0)

def show7():
	GPIO.output(31, 0)
	GPIO.output(33, 0)
	GPIO.output(35, 0)

def show8():
	number = [31, 33, 29, 23, 21, 35, 19]
	GPIO.output(number, 0)

def show9():
	number = [29, 31, 33, 23, 35, 19]
	GPIO.output(number, 0)

def show0():
	number = [31, 33, 35, 19, 21, 29]
	GPIO.output(number, 0)

#------------- interupt loogika ---------------------------------------
GPIO.add_event_detect(15, GPIO.FALLING, callback=bttn_callback, bouncetime=100)
signal.signal(signal.SIGINT, signal_handler)
signal.pause

#------------- muutujad, mida kasutatakse numbrite loendamise loogikas
activeNumber = 1
suund = 1
vaheaeg = 1
GPIO.output(pins, 1)
while(True):
#------------- loogika numberite näitamiseks--------------------------
	if activeNumber == 1:
		show1()
	elif activeNumber == 2:
		show2()
	elif activeNumber == 3:
		show3()
	elif activeNumber == 4:
		show4()
	elif activeNumber == 5:
		show5()
	elif activeNumber == 6:
		show6()
	elif activeNumber == 7:
		show7()
	elif activeNumber == 8:
		show8()
	elif activeNumber == 9:
		show9()
	else:
		show0()
	sleep(vaheaeg)
	GPIO.output(pins, 1)

#--------------- siit suunavahetus ---------------

	if suund == 1:
		activeNumber += 1
		if activeNumber >= 10:
			activeNumber = 0
	elif suund == 2:
		activeNumber -= 1
		if activeNumber <= -1:
			activeNumber = 9
	elif suund == 3:
		activeNumber = randint(1, 9)
print("done")
GPIO.cleanup(pins)

#!/usr/bin/python3
import socket
import select
import sys
from _thread import *

class Blinker:  #ülesanne 1.2 prax 1
	def __init__(self, sleepTime = 0.5):
		'''try:
			import RPi.GPIO as GPIO
		except RuntimeError:
			print("...error importing RPi.GPIO module")'''
		print("Blink initialized")
		self.sleepTime = sleepTime
		self.GPIO = GPIO

	def setSleepTime(self, time):
		self.sleepTime = time
		print("Set sleepTime to: "+str(self.sleepTime))

	def getSleepTime(self):
		print(self.sleepTime)

	def main(self):
		from time import sleep

		self.GPIO.setmode(GPIO.BOARD)
		pins=[36, 38]
		self.GPIO.setup(pins, GPIO.OUT)
		self.GPIO.output(36, 1)
		self.GPIO.output(38, 0)
		print("on")
		sleep(self.sleepTime)
		self.GPIO.output(36, 0)
		self.GPIO.output(38, 1)
		print("off")
		sleep(self.sleepTime)
		print(self.sleepTime)

	def stop(self):
		print("stopping")
		#self.GPIO.cleanup(pins)

class LedSegmentDisplay:
	from time import sleep
	import sys
	import signal
	from random import randint

	def __init__(self, pins = [37, 35, 33, 31, 29, 23, 21, 19], suund = 1, activeNumber = 1, vaheaeg = 1):
		print("7-segment display initialized")
		# ------------pinnide setup-----------
		try:
			import RPi.GPIO as GPIO
		except RuntimeError:
			print("...error importing RPi.GPIO module")
		self.GPIO = GPIO
		self.pins = pins
		self.suund = suund
		self.activeNumber = activeNumber
		self.vaheaeg = vaheaeg

	def main(self):
		self.GPIO.setmode(GPIO.BOARD)
		self.GPIO.setup(pins, GPIO.OUT)
		self.GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		# ------------- interupt loogika ---------------------------------------
		self.GPIO.add_event_detect(15, GPIO.FALLING, callback=bttn_callback, bouncetime=100)
		signal.signal(signal.SIGINT, signal_handler)
		signal.pause

		# ------------- muutujad, mida kasutatakse numbrite loendamise loogikas
		self.GPIO.output(pins, 1)
		while (True):
			# ------------- loogika numberite näitamiseks--------------------------
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
			#---------------siit suuna vahetus--------------------
			if self.suund == 1:
				self.activeNumber += 1
				if self.activeNumber >= 10:
					self.activeNumber = 0
			elif self.suund == 2:
				self.activeNumber -= 1
				if self.activeNumber <= -1:
					self.activeNumber = 9
			elif self.suund == 3:
				self.activeNumber = randint(1, 9)

	# -----------btn interrupt-----------
	def signal_handler(self, sig, frame):
		self.GPIO.cleanup()
		self.GPIO.exit(0)

	def bttn_callback(self,channel):
		global suund
		print("nupp")
		if suund == 1:
			suund = 2
		elif suund == 2:
			suund = 3
		elif suund == 3:
			suund = 1
		print(suund)

	# -----------mis pin on mis numbril tähtis---------
	def show1(self):
		self.GPIO.output(33, 0)
		self.GPIO.output(35, 0)

	def show2(self):
		number = [31, 33, 23, 21, 19]
		self.GPIO.output(number, 0)

	def show3(self):
		number = [31, 33, 23, 35, 19]
		self.GPIO.output(number, 0)

	def show4(self):
		number = [29, 23, 33, 35]
		self.GPIO.output(number, 0)

	def show5(self):
		number = [31, 29, 23, 35, 19]
		self.GPIO.output(number, 0)

	def show6(self):
		number = [31, 29, 23, 35, 19, 21]
		self.GPIO.output(number, 0)

	def show7(self):
		self.GPIO.output(31, 0)
		self.GPIO.output(33, 0)
		self.GPIO.output(35, 0)

	def show8(self):
		number = [31, 33, 29, 23, 21, 35, 19]
		self.GPIO.output(number, 0)

	def show9(self):
		number = [29, 31, 33, 23, 35, 19]
		self.GPIO.output(number, 0)

	def show0(self):
		number = [31, 33, 35, 19, 21, 29]
		self.GPIO.output(number, 0)

	print("done")
	GPIO.cleanup(pins)
Blinker = Blinker()
LedDisplay = LedSegmentDisplay()
listenPort = input("Enter the port to listen to: ")
HOST = ''
if listenPort != "":
	PORT = int(listenPort)
else:
	PORT = 8888
numconn = 10
buffer_size = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('---Scoket created---')

#bind socket to a local host and port
try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print('---bind failed ... error code: ' + str(msg.args[0])+ ', error message: ' + msg.args[1])
	sys.exit()

print('---Socket bind complete---')

#make socket to listne to incomming connections
s.listen(numconn)
print('---Socket is now listening---')

#fn for handling connections... this will be used to create threads
def clientthread(conn):
	conn.setblocking(0)
	eelnevData = ""
	eelnevReply = ""
	sisenevData = ""
	#sending messages to connected clients
	conn.send('willkommen auf meinem server, kirjuta midagi ja vajuta enter... \n'.encode()) #send only takses bytes
	while True:
		
		try:	#recive data from client
			
			if eelnevData == "start":
				Blinker.main()

			elif eelnevData == "stop":
				Blinker.stop()
				eelnevData = ""

			ready = select.select([conn],[], [], 0.01)
			if ready[0]:  #https://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
				data = conn.recv(buffer_size)
				if not data:
					print("---breaking connection---")
					break
				if data.decode() != sisenevData:
					sisenevData = data.decode()
				elif data.decode() == sisenevData:
					continue
				if sisenevData in ["start", "stop"]:
					eelnevData = sisenevData
					sisenevData = ""
				if str(sisenevData).isnumeric():
					print("isnumeric!")
					Blinker.setSleepTime(int(sisenevData))
					sisenevData = ""
				if sisenevData[:2] == "0.":
					if sisenevData[2:].isnumeric():
						print("isnumeric!")
						Blinker.setSleepTime(float("0."+sisenevData[2:]))
						sisenevData = ""

				reply = '---OK---' + data.decode() #encode bytes to string
				conn.sendall(reply.encode())
				print('recived: '+data.decode())

				print('replied: '+reply)

				print()
		except socket.error as message:
			print(message)
			break
	conn.close()
while True:
	#wait to accept a connection - blocking call
	conn, addr = s.accept()

	#display client info
	print('---connected with '+ addr[0] +':' + str(addr[1]))
	start_new_thread(clientthread, (conn, ))
s.close()

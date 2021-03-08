#!/usr/bin/python3
import socket
import select
import sys
from _thread import *
try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("---error importing GPIO module---")


class Blinker:  #ülesanne 1.2 prax 1

	sleeptime = 0.5
	def __init__(self, sleepTime = 0.5):
		print("Blink initialized")
		self.sleepTime = sleepTime
		self.GPIO = GPIO
		self.pins = pins=[36, 38]

	def setSleepTime(self, time):
		self.sleepTime = time
		print("Set sleepTime to: "+str(self.sleepTime))

	def getSleepTime(self):
		print(self.sleepTime)

	def main(self):
		from time import sleep
		global GPIO
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.pins, GPIO.OUT)
		GPIO.output(36, 1)
		GPIO.output(38, 0)
		print("on")
		sleep(self.sleepTime)
		GPIO.output(36, 0)
		GPIO.output(38, 1)
		print("off")
		sleep(self.sleepTime)
		print(self.sleepTime)

	def stop(self):
		print("stopping")
		GPIO.cleanup(self.pins)

class LedSegmentDisplay: #Prax1 ül 1.3
	import sys
	import signal

	def __init__(self, pins = [37, 35, 33, 31, 29, 23, 21, 19], suund = 1, activeNumber = 1, vaheaeg = 1):
		print("7-segment display initialized")
		# ------------pinnide setup-----------
		self.GPIO = GPIO
		self.pins = pins = [37, 35, 33, 31, 29, 23, 21, 19]
		self.suund = suund = 1
		self.activeNumber = activeNumber = 1
		self.vaheaeg = vaheaeg = 1

	def main(self):
		from time import sleep
		from random import randint
		self.GPIO.setmode(GPIO.BOARD)
		self.GPIO.setup(self.pins, GPIO.OUT)
		self.GPIO.output(self.pins, 1)

		# ------------- loogika numberite näitamiseks--------------------------
		if self.activeNumber == 1:
			self.show1()
		elif self.activeNumber == 2:
			self.show2()
		elif self.activeNumber == 3:
			self.show3()
		elif self.activeNumber == 4:
			self.show4()
		elif self.activeNumber == 5:
			self.show5()
		elif self.activeNumber == 6:
			self.show6()
		elif self.activeNumber == 7:
			self.show7()
		elif self.activeNumber == 8:
			self.show8()
		elif self.activeNumber == 9:
			self.show9()
		else:
			self.show0()
		sleep(self.vaheaeg)
		self.GPIO.output(self.pins, 1)
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
	def ChangeSuund(self):
		self.suund +=1
		if self.suund == 4:
			self.suund = 1

	# -----------btn interrupt-----------
	def signal_handler(self, sig, frame):
		self.GPIO.cleanup()
		self.GPIO.exit(0)

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

	def stop(self):
		print("done")
		GPIO.cleanup(self.pins)

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
	activePrograms = []
	#sending messages to connected clients
	conn.send('willkommen auf meinem server, kirjuta midagi ja vajuta enter... \n'.encode()) #send only takses bytes
	while True:
		
		try:	#recive data from client
			
			if eelnevData == "start1":
				Blinker.main()
				activePrograms.append(1)
			elif eelnevData == "stop1":
				Blinker.stop()
				eelnevData = ""
				activePrograms.remove(1)
			if eelnevData == "start2":
				LedDisplay.main()
				activePrograms.append(2)
			elif eelnevData == "stop2":
				LedDisplay.stop()
				eelnevData = ""
				activePrograms.remove(2)

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
				if sisenevData in ["start1", "stop1", "start2", "stop2"]:
					errReply = "---can't run, program already in use!---"
					if sisenevData == "start1":
						if 1 in activePrograms:
							print(errReply)
							conn.sendall(errReply.encode())
							continue
					if sisenevData == "start2":
						if 2 in activePrograms:
							print(errReply)
							conn.sendall(errReply.encode())
							continue
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
				if sisenevData == "bttn":
					LedDisplay.ChangeSuund()
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

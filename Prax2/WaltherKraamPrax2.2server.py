#!/usr/bin/python3
import socket
import sys
from _thread import *

class Blinker:  #ülesanne 1.2 prax 1
	def __init__(self, sleepTime = 0.5):
		try:
			import RPi.GPIO as GPIO
		except RuntimeError:
			print("...error importing RPi.GPIO module")
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
		sleep(self.sleepTime)
		self.GPIO.output(36, 0)
		self.GPIO.output(38, 1)
		sleep(self.sleepTime)
		print(self.sleepTime)
	def stop(self):
		self.GPIO.cleanup(pins)
Blinker = Blinker()
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
	eelnevData = ""
	#sending messages to connected clients
	conn.send('willkommen auf meinem server, kirjuta midagi ja vajuta enter... \n'.encode()) #send only takses bytes
	while True:
		
		try:	#recive data from client
			
			if eelnevData == "start":
				Blinker.main()

			elif eelnevData == "stop":
				Blinker.stop()

			print("start of line")
			data = conn.recv(buffer_size)
			if not data:
				print("---breaking connection---")
				break
			sisenevData = data.decode()
			if sisenevData == "start" or "stop":
				eelnevData = sisenevData
			if str(sisenevData).isnumeric():
				print("isnumeric!")
				Blinker.setSleepTime(int(sisenevData))
			if sisenevData[:2] == "0.":
				if sisenevData[2:].isnumeric():
					print("isnumeric!")
					Blinker.setSleepTime(float("0."+sisenevData[2:]))
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

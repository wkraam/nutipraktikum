#!/usr/bin/python3
import socket
import sys
from _thread import *

HOST = ''
PORT = 8888
numconn = 10
buffer_size = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
	#sending messages to connected clients
	conn.send('wilcommen aus meiner server, kirjuta midagi ja vajuta enter... \n'.encode()) #send only takses bytes
	while True:
		try:
			#recive data from client
			data = conn.recv(buffer_size)
			if not data:
				break
			reply = '---OK---'+data.encode() #encode bytes to string
			conn.sendall(reply.encode())
			print('recived: ')
			print(data.decode())
			print('sent: ')
			print(reply)
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

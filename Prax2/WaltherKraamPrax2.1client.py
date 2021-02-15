#!/usr/bin/python
import socket
import sys

host = '172.17.54.208'
port = 8888
message = "Hallo friend"
buffer_size = 4096

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
	print('---failed to create socket, error code: ' + str(msg.args[0]) + ' error message: ' + msg.args[1])
	sys.exit

print('---socket created')

try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print('---hostname could not be resolved, exiting')
	sys.exit()

print('---IP address of ' + host + ' is ' + remote_ip)

#connect to remote server
s.connect((remote_ip, port))

print('---Socket connected to '+host+' is '+remote_ip)

try:
	#send string encoded as byte
	s.sendall(message.encode())
except socket.error:
	#send failed
	print('---send failed---')
	sys.exit()

print(message)
print('---message sent successfully---')

#now recive data
reply = s.recv(buffer_size).decode()

print(reply)

#close the socket
s.close()

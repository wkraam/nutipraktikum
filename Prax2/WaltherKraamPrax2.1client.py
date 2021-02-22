#!/usr/bin/python
import socket
import sys

hostSisestus = input("Sisesta ip aadress: ")
if hostSisestus == "":
	host = '172.17.55.53'
else:
	host = hostSisestus
portSisestus = input("Sisesta port (rasbperrypi default = 8888): ")
if portSisestus == "":
	port = 8888
else:
	port = int(portSisestus)
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

reply = s.recv(buffer_size).decode()
print(reply)

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

while True:
	#
	edastusTekst = input("")
	#proovin seda saata
	if edastusTekst != "":
		try:
			s.sendall(edastusTekst.encode())
		except socket.error:
			print("---send failed---")
			sys.exit()
		print("sent message: "+edastusTekst)
		print("---Message sent successfully---")
		
		#recive data
		reply = s.recv(buffer_size).decode()
		print(reply)
	else:
		break
#close the socket
s.close()

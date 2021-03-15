#!/usr/bin/python3

import serial, time, sys
try:
    ser=serial.Serial('/dev/ttyUSB0', 9600)
    print(ser.name)
    while True:
        read_serial=ser.readline().decode()
        print(read_serial.rstrip('\n'))
        sisend = input("sisesta '1' -LED tööle panna / '0' -LED kustutada ").encode('UTF-8')
        ser.write(sisend)
except KeyboardInterrupt:
    ser.close()
    print("ending due to keyboard interrupt")
    sys.exit()
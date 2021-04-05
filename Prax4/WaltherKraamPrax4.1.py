#!/usr/bin/python3
# koostas Walther Kraam
import serial, time, sys
try:
    ser=serial.Serial('/dev/rfcomm0', 9600)
    print(ser.name)
    while True:
        write_ser=input("Sisesta saade: ").encode(encoding='UTF-8')
        ser.write(write_ser)
        ser.write(b', ')
        read_ser=ser.read().decode(encoding='UTF-8')
        print(read_ser)
except KeyboardInterrupt:
    ser.close()
    print('ending due to keyboard interrupt')
    sys.exit()

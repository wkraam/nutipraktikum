#!/usr/bin/python3
# koostas Walther Kraam
import serial, time, sys, RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT)
led_status = 'off'

try:
    ser=serial.Serial('/dev/rfcomm0', 9600, timeout = 2)
    print(ser.name)
    ser.write(b'sisesta 1 et led toole panna, 2 et led kustutada, 3 et olekut teada saada')
    while True:
        read_ser=ser.read(1).decode(encoding='UTF-8')
        print(read_ser)
        if read_ser == '1':
            print('led tööle')
            led_status = 'on'
        if read_ser == '2':
            print('led kustu')
            led_status = 'off'
        if read_ser == '3':
            print(led_status)
            if led_status == 'on':
                ser.write(b'led on sees')
            else:
                ser.write(b'led on valjas')
        if led_status == 'on':
            GPIO.output(38, 1)
        if led_status == 'off':
            GPIO.output(38, 0)
except KeyboardInterrupt:
    ser.close()
    print('ending due to keyboard interrupt')
    sys.exit()

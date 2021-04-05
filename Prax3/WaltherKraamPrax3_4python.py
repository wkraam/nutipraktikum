#!/usr/bin/python3

import serial, time, sys, board
import i2c_lcd
lcd = i2c_lcd.lcd()
signal = 0
out = 0

try:
    ser=serial.Serial('/dev/ttyUSB0', 9600)
    print(ser.name)
    while True:
        signal = ser.readline().decode()
        signal = signal.strip()
        out = 5/1024*int(signal)
        out = round(out, 2)
        print(signal)
        lcd.lcd_clear()
        lcd.lcd_display_string(str(out)+'V', 1)
        time.sleep(0.2)
except KeyboardInterrupt:
    ser.close()
    lcd.lcd_clear()
    print("ending due to keyboard interrupt")
    sys.exit()
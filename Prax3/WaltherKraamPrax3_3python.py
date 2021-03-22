#!/usr/bin/python3

import serial, time, sys, board, neopixel, matplotlib
import matplotlib.pyplot as plt
import numpy as np
#pixels = neopixel.NeoPixel(board.D18, 1)
#pixels.fill((0, 0, 0))

temp = 0
ledVal = 0
tempArr = [0]
cnt = 0
cntArr = [0]
file = open("temperatures.txt", "at")
x = cntArr
y = tempArr
plt.ion()
figure, ax = plt.subplots(figsize=(8,6))
line1, = ax.plot(x, y)
plt.ylabel("Temperature")
plt.xlabel("Time")

try:
    ser=serial.Serial('/dev/ttyUSB0', 9600)
    print(ser.name)
    while True:
        temp = ser.readline().decode()
        temp = float(temp.rstrip('\n'))
        temp = int(temp*10)
        tempArr.append(temp/10)
        
        #ledVal = 0.7058823529412*temp # = range(180 - 360)
        #ledVal = 0.3921568627451*temp # = range(260 - 360)
        if ledVal > 255.0:
            ledVal = 255
        if ledVal < 0.0:
            ledVal = 0
        ledValR = ledVal-70
        if ledValR > 255.0:
            ledValR = 255
        if ledValR < 0.0:
            ledValR = 0
            
        print(str(temp/10) + "C " + str(ledVal)+' '+str(tempArr))
        #pixels.fill((ledValR, 0, 255-ledVal))
        file.write(str(temp/10)+'\n')

        line1.set_ydata(tempArr)
        line1.set_xdata(cntArr)
        figure.canvas.draw()
        figure.canvas.flush_events()
        
        cnt += 1
        cntArr.append(cnt)
        time.sleep(0.8)
except KeyboardInterrupt:
    file.close()
    ser.close()
    print("ending due to keyboard interrupt")
    sys.exit()

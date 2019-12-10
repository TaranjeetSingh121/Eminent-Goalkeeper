# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 14:42:03 2019

@author: singh
"""
import serial
# import syslog
import time



# port = 'Port_#0001.Hub_#0001'
serPort = 'COM5'
baudRate = 9600
with serial.Serial(serPort, baudRate, timeout=1) as ser:
    time.sleep(5)
    print('input:1')
    ser.write(1)
    time.sleep(5)
    print('input 5')
    ser.write(5)
    ser.close()
#waitForArduino()









#print ("Python value sent B ")

#ard.write(b'B')
#ard.close()

# exit()
# ard.write('S')
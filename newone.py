# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:21:54 2019

@author: singh
"""


import serial
import time

# Define the serial port and baud rate.
# Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
ser = serial.Serial('COM5', 9600)

def led_on_off():
    
        print("Backward...")
        time.sleep(0.1) 
        ser.write(b'2') 
        print("Brake...")
        time.sleep(5)
        ser.write(b'5')

        print("Program Exiting")
        ser.close()
        
time.sleep(2) # wait for the serial connection to initialize

led_on_off()
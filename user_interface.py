"""
============================================================

                         HTTP 418
               CSE 4316/4317 - Senior Design
            The University of Texas at Arlington
    Dylan Bryce, Biraj GC, Preston Mann, Isabel Metevier

============================================================

 File: user_interface.py

 Brief: Displays lights and takes input to "turn on" neural network

 Revision History:
 Date       | Engineer     | Description
 -----------|--------------|--------------------------------
 10-22-2022 | Metevier, I. | add light methods
            |              |
 -----------|--------------|--------------------------------
 11-08-2022 | Metevier, I. | add turnWhite() & turnPink() 
            |              | and modify button to switch 
            |              | methods
 -----------|--------------|--------------------------------
            |              | 
============================================================
"""
import smbus
import time
import os

i2cbus = smbus.SMBus(1)

#Eight GPIO Values on GPIO Expander are written as ful byte 0xFF-0x00
#Use these values when driving as Active High
#LEDREDP0 = 0x01  #0000 0001
#LEDYELP1 = 0x02  #0000 0010
#LEDGRNP2 = 0x04  #0000 0100
#LEDRYGON = 0x07  #0000 0111
#LEDOFFPX = 0x00  #0000 0000

def turnRed():
    i2cbus.write_byte(0x20,LEDREDP0)
def turnGreen():
    i2cbus.write_byte(0x20, LEDGRNP2)
def turnYellow():
    i2cbus.write_byte(0x20, LEDYELP1)
def turnOff():
    i2cbus.write_byte(0x20, LEDOFFPX)
def turnWhite():
    i2cbus.write_byte(0x20, LEDWHITEP4)
def turnPink():
    i2cbus.write_byte(0x20, LEDPINKP3)

def waitForSwitch():
    i2cbus.write_byte(0x21, 0xFF)
    turnOff()
    button = 0xFF #not pushed
    turnYellow() #AT STANDBY waiting for button pushed
    while button == 0xFF:
        button = i2cbus.read_byte(0x21)
        time.sleep(1.0)

# frequent enough of a check in order to coinside with user input
# When low, it's on
def checkOffSwitch():
    button = i2cbus.read_byte(0x21)
    if button != 0xFF:
        print("Turned On")
        return True
    else:
        print("Turned Off")
        return False
        
#Use these values when driving as Active Low, necessary with PNP Transistor
LEDREDP0 = 0xFE  #1111 1110
LEDYELP1 = 0xFD  #1111 1101
LEDGRNP2 = 0xFB  #1111 1011
LEDRYGON = 0xF8  #1111 1000
LEDOFFPX = 0xFF  #1111 1111

LEDPINKP3 = 0XF7
LEDWHITEP4 = 0XEF


""" 
#Testing Lights
while True:
        turnRed()
        time.sleep(0.5)
        turnYellow()
        time.sleep(0.5)
        turnGreen()
        time.sleep(0.5)
        turnOff()
        
        time.sleep(1.0)
        i2cbus.write_byte(0x20, LEDRYGON)
        time.sleep(1.0)
        i2cbus.write_byte(0x20, LEDOFFPX)
        time.sleep(0.5)

#Testing Button
waitForSwitch()
while True:
    if !checkOffSwitch():
        turnYellow()
        break()
"""

isRunning = False

#initial wait/start
waitForSwitch()
turnGreen()

while True:
    if checkOffSwitch():
        if isRunning:
            continue
        else:
            #start program
            os.system('python main.py')
            isRunning = True
            turnGreen()
    else:
        if isRunning:
            #kill process
            isRunning = False
            waitForSwitch()
        else:
            continue
    

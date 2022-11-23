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
 Date       | Engineer     | Description
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

#Use these values when driving as Active Low, necessary with PNP Transistor
LEDREDP0 = 0xFE  #1111 1110
LEDYELP1 = 0xFD  #1111 1101
LEDGRNP2 = 0xFB  #1111 1011
LEDRYGON = 0xF8  #1111 1000
LEDOFFPX = 0xFF  #1111 1111

LEDPINKP3 = 0XF7
LEDWHITEP4 = 0XEF

class UI:
    def __init__(self):
        self.i2cbus = smbus.SMBus(1)
    
    def turnRed(self):
        self.i2cbus.write_byte(0x20,LEDREDP0)
    def turnGreen(self):
        self.i2cbus.write_byte(0x20, LEDGRNP2)
    def turnYellow(self):
        self.i2cbus.write_byte(0x20, LEDYELP1)
    def turnOff(self):
        self.i2cbus.write_byte(0x20, LEDOFFPX)
    def turnWhite(self):
        self.i2cbus.write_byte(0x20, LEDWHITEP4)
    def turnPink(self):
        self.i2cbus.write_byte(0x20, LEDPINKP3)

    def waitForSwitch(self):
        self.i2cbus.write_byte(0x21, 0xFF)
        self.turnOff()
        button = 0xFF #not pushed
        self.turnYellow() #AT STANDBY waiting for button pushed
        while button == 0xFF:
            button = self.i2cbus.read_byte(0x21)
            time.sleep(1.0)

    # frequent enough of a check in order to coinside with user input
    # When low, it's on
    def checkOffSwitch(self):
        button = self.i2cbus.read_byte(0x21)
        if button != 0xFF:
            return True
        else:
            return False
        
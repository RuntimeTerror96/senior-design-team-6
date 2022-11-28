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
 11-22-2022 | Metevier, I. | modify to be a class
            |              |             
------------|--------------|--------------------------------
 11-28-2022 | Metevier, I. | added Doxygen Instructions
            |              |
============================================================
"""
import smbus
import time

## @brief Using these values when driving as Active Low, necessary with PNP Transistor
LEDREDP0 = 0xFE     #1111 1110
LEDYELP1 = 0xFD     #1111 1101
LEDGRNP2 = 0xFB     #1111 1011
LEDRYGON = 0xF8     #1111 1000
LEDOFFPX = 0xFF     #1111 1111

LEDPINKP3 = 0XF7    #1111 0111
LEDWHITEP4 = 0XEF   #1110 1111

## @brief This class controls the User Interface with AV-I 
class UI:
    
    ## @brief Default Constructor
    def __init__(self):
        self.i2cbus = smbus.SMBus(1)
    
    ## @brief Changes the light to red on the traffic light extender
    ## @parm UI self - The object that the method is being called upon
    def turnRed(self):
        self.i2cbus.write_byte(0x20,LEDREDP0)
    
    
    ## @brief Changes the light to green on the traffic light extender
    ## @parm UI self - The object that the method is being called upon
    def turnGreen(self):
        self.i2cbus.write_byte(0x20, LEDGRNP2)
        
    
    ## @brief Changes the light to yellow on the traffic light extender
    ## @parm UI self - The object that the method is being called upon
    def turnYellow(self):
        self.i2cbus.write_byte(0x20, LEDYELP1)
    
    ## @brief Turn off all lights on the car
    ## @parm UI self - The object that the method is being called upon
    def turnOff(self):
        self.i2cbus.write_byte(0x20, LEDOFFPX)
        
    ## @brief Turns on additional white light
    ## @parm UI self - The object that the method is being called upon
    def turnWhite(self):
        self.i2cbus.write_byte(0x20, LEDWHITEP4)
    
    ## @brief Turns on additional white light
    ## @parm UI self - The object that the method is being called upon
    def turnPink(self):
        self.i2cbus.write_byte(0x20, LEDPINKP3)

    ## @brief Stays in standby until the switch is in the "on" position
    ## @parm UI self - The object that the method is being called upon
    def waitForSwitch(self):
        self.i2cbus.write_byte(0x21, 0xFF)
        self.turnOff()
        button = 0xFF #not pushed
        self.turnYellow() #AT STANDBY waiting for button pushed
        while button == 0xFF:
            button = self.i2cbus.read_byte(0x21)
            time.sleep(1.0)

    ## @brief Checks if the switch is in the "on" position
    ## @parm UI self - The object that the method is being called upon
    ## @return bool - True if in "on" position, False if in "off" position
    # frequent enough of a check in order to coinside with user input
    # When low, it's on
    def checkOffSwitch(self):
        button = self.i2cbus.read_byte(0x21)
        if button != 0xFF:
            return True
        else:
            return False
        
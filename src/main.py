#============================================================
#
#                         HTTP 418
#               CSE 4316/4317 - Senior Design
#            The University of Texas at Arlington
#    Dylan Bryce, Biraj GC, Preston Mann, Isabel Metevier
#
#------------------------------------------------------------
#
# File: main.py
#
# Brief: This file is our main it will run our program 
#        Model will not be trained in this file 
#        
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 09-26-2022 | Mann, P.     | Initial Release
# 10-10-2022 | Bryce, D.    | Added camera driver code
# 10-14-2022 | Bryce, D.    | Refactored main code into a new
#                           | class (AVI)
# 10-28-2022 | Bryce, D.    | Added vehicle control
#
#============================================================

import sys 
import numpy as np
import cv2 as cv
from Camera import Camera
from ImageProcessor import ImageProcessor
from FakeNeuralNetwork import FakeNeuralNetwork # FIXME: testing only, replace with real model
#import ModelReconciliator
from SunFounder_PiCar import picar

class AVI:
    def __init__(self, DEBUG=False):
        self.DEBUG = DEBUG

        # setup the camera
        self.camSrc = 0
        print("DEBUG: setting up camera on source " + str(self.camSrc))
        self.cam = Camera(self.camSrc)

        picar.setup()

        # Setup the camera servos
        self.panServo = picar.Servo.Servo(1)
        self.panServo.offset = -30  # calibrate servo to center TODO might need tuning
        self.panServo.write(90)

        self.tiltServo = picar.Servo.Servo(2)
        self.tiltServo.offset = 20  # calibrate servo to center TODO might need tuning
        self.tiltServo.write(90)

        # Setup the back wheels
        self.backWheels = picar.back_wheels.Back_Wheels()
        self.backWheels.speed = 0

        # Setup the front wheels
        self.frontWheels = picar.front_wheels.Front_Wheels()
        self.frontWheels.turning_offset = -25 # calibrate servo to center TODO may need tuning
        self.frontWheels.turn(90)

        # setup the image processor
        self.imgProcessor = ImageProcessor()

        # setup the neural network
        # FIXME: replace with real model
        self.fNN = FakeNeuralNetwork()

        # setup the model reconciliator
        # FIXME: model reconciliator may need rework
        #self.modelRec = ModelReconciliator()

    # TODO i think we can just call this method to kick the whole thing off.
    def Drive(self, initialSpeed=0):
        
        # start the camera
        self.cam.startCamera()

        # NOTE: command structure (list)
        #       command[0] - steering angle (float)
        #       command[1] - motor command (1 = go, 0 = stop)
        #       command[2] - speed (float) <- TODO: implemented once if we get to object recognition
        commands = [None] * 3
        commands[2] = initialSpeed


        try:
            while True:
                # Stop if the user presses "q" TODO: we need some other way to stop this.
                # Some thoughts: we could make a bool called "stop" or something. initialize it to false,
                # and then every function that we call can return a bool. i.e.
                #       stop = self.imgProcessor.extractLines(frame)
                # and then we know that if that function returns true (or whatever), that something went wrong and we
                # can break out of the infinite loop.
                if (cv.waitKey(1) == ord("q")) or self.cam.stopped:
                    self.cam.stopCamera()
                    break

                # get the frame
                frame = self.cam.frame

                # process the frame
                # FIXME: eventually this will return lane lines. Updates need to be made to ImageProcessor.py
                laneLines = self.imgProcessor.extractLines(frame)

                # Use the path finding model to get the steering angle from the lange lines
                # FIXME: replace with real model
                steeringAngle = self.fNN.GetAngle(laneLines)

                # TODO: use the object detection model to get ????
                #       model will probably give go/stop decision, speed decision, and maybe a different steering angle to avoid an object? idk

                # Use the ModelReconciliator to make a final decision based on output from both models
                # FIXME: right now i'm skipping this step for testing since modelRec may need rework
                # pseudo code:
                #   commands = self.modelRec.makeDecision(steeringAngle, objdetectoutput)


                commands[0] = steeringAngle
                commands[1] = None
                commands[2] = 0

                # Send motor and servo commands with the output from ModelReconciliator
                self.frontWheels.turn(commands[0])
                self.backWheels.speed = commands[2]



                if self.DEBUG == True:
                    cv.imshow("Video", frame)
                    cv.imshow("Processed", laneLines)

        # catch ctrl+c from terminal, shutdown gracefully
        except KeyboardInterrupt:
            self.cam.stopCamera()
            self.frontWheels.turn(90)
            self.backWheels.speed = 0


########## Main ##########
def main():

    # Get command line arguments
    nArgc = len(sys.argv)
    nArgv = sys.argv

    # check for debug flag
    if nArgc > 1 and nArgv[1] == "-d":
        DEBUG = True
    else:
        DEBUG = False
    
    if DEBUG:
        print("main is running")
        print("python version: ",sys.version)
        print("numpy version: ",np.__version__)

    vehicle = AVI(DEBUG)
    
    vehicle.Drive()

if __name__ == "__main__":
    main()
    
    # sys.exit(main())  <-- not sure why but the camera code didn't work with this.

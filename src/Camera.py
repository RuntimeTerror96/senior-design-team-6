#============================================================
#
#                         HTTP 418
#               CSE 4316/4317 - Senior Design
#            The University of Texas at Arlington
#    Dylan Bryce, Biraj GC, Preston Mann, Isabel Metevier
#
#============================================================
#
# File: Camera.py
#
# Brief: This file contains all of the classes related to the
#        Image Processing Layer
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 09-25-2022 | Bryce, D     | Initial Release
#
#============================================================

import cv2 as cv
import time
from multiprocessing import Process

## @brief This class contains driver code for interfacing with the camera.
## Camera is a singleton class so only one istance of a Camera object
## can be created. This class contains all needed functions to connect
## to and interface with the camera.
class Camera(object):

    # Private variables
    __videoSource = 0
    __cam = None
    __camProc = None
    __myVar = 1

    ## @brief Default constructor enforcing the singleton pattern.
    ## If a Camera object already exists, this function returns a reference
    ## to that object. Else, it creates a new Camera object.
    ## @param Camera cls - The object being created (leave this blank when calling the function)
    ## @return Camera cls - A Camera object
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Camera, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.__videoSource = 0
        self.__cam = None
        self.__camProc = None
        self.__myVar = 1
        pass

    def openCamera(self):
        # check to see if camera is already open
        if self.__cam is not None:
            print("WARN: Camera already open")
            return

        # open camera
        self.__cam = cv.VideoCapture(self.__videoSource)

        # verify camera open success
        if not self.__cam.isOpened():
            print ("ERROR: Could not open camera.")
            # TODO: exit program, return, do something, idk. also set status indicator light

        # set the width and height of the video capture
        frameWidth = 320
        frameheight = 240
        self.__cam.set(cv.CAP_PROP_FRAME_WIDTH, frameWidth)
        self.__cam.set(cv.CAP_PROP_FRAME_HEIGHT, frameheight)

        self.__cam.set(cv.CAP_PROP_BUFFERSIZE,1)
        cv.setUseOptimized(True)

        return

    def startCamera(self):
        self.__camProc = Process(target=Camera.captureData(self))
        self.__camProc.start()

    def captureData(self):
        self.__myVar = 2
        while self.__cam.isOpened():
            ret, frame = self.__cam.read()
            cv.imshow('frame', frame)

    # TODO: for multi process, this function probably needs to stop the process.
    def closeCamera(self):

        print(self.__myVar)

        # kill the captureData process
        if self.__camProc is not None and self.__camProc.is_alive():
            # DEBUG
            print("captureData is alive, terminating...")
            self.__camProc.terminate()
            print("captureData terminated")
        else:
            print("captureData was not alive.")

        # if camera is not open, report a warning and return.
        if not self.__cam.isOpened():
            print ("WARN: Camera not open.")
            return
        
        # else, close the connection.
        self.__cam.release()

        # DEBUG
        print("returning from closeCamera")

        return

# Debug
if __name__ == "__main__":
    cam = Camera()

    cam.openCamera()

    cam.startCamera()
    #cam.captureData()

    time.sleep(10)
    cam.closeCamera()

    

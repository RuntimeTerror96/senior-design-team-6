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
# Brief: This file defines a class that allows the code to
#        connect to and retrieve images from the camera which
#        runs in a seperate thread.
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 09-25-2022 | Bryce, D     | Initial Release
#
#============================================================

import cv2
from threading import Thread

## @brief This class contains driver code for interfacing with the camera.
## This class contains all needed functions to connect
## to and interface with the camera.
class Camera:
    ## @brief Initialize the camera object and setup the stream.
    ## @param Int camSrc - the identifier of the camera to be used. This will likely always be 0
    def __init__(self, camSrc=0):

        # Setup CV2 video capture
        self.stream = cv2.VideoCapture(camSrc)

        # verify camera open success
        if not self.stream.isOpened():
            print ("ERROR: Could not open camera.")
            # TODO: set status indicator light

        # set the width and height of the video
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH,320) # width
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT,240) # height

        # amount of frames stored in CV2's internal buffer at a time
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE,1)

        # set cv2 to optimized mode (not really sure what this does)
        cv2.setUseOptimized(True)

        # read the first frame (not sure why but this needs to
        # be done once before real video reading starts)
        (self.captured, self.frame) = self.stream.read()

        # variable to indicate the status of the capture. Set
        # this to True to stop the capture.
        self.stopped = False

    ## @brief Spawns a new thread to run the camera stream.
    ## @return The camera object running in the new thread.
    def startCamera(self):
        Thread(target=self.captureFrame, args=()).start()
        return self

    ## @brief Reads (captures) a frame from the stream.
    def captureFrame(self):

        while not self.stopped:
            if not self.captured:
                self.stopCamera()
            else:
                (self.captured, self.frame) = self.stream.read()

    ## @brief Stops the camera stream.
    def stopCamera(self):
        self.stopped = True




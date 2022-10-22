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
#
#============================================================

import sys 
import numpy as np
import cv2 as cv
import Camera
import ImageProcessor
import picar

print("python version: ",sys.version)
print("numpy version: ",np.__version__)

class AVI:
    def __init__(self):
        
        # setup the camera
        self.camSrc = 0
        print("DEBUG: setting up camera on source " + str(self.camSrc))
        self.cam = Camera(self.camSrc)

        # TODO setup the camera servo(s)

        # TODO setup the back wheels

        # TODO setup the front wheels

        # setup the image processor
        self.imgProcessor = ImageProcessor()

    # TODO i think we can just call this method to kick the whole thing off.
    def Drive(self):
        
        # start the camera
        self.cam.startCamera()

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
            detectedLines = self.imgProcessor.extractLines(frame)

            # TODO: here we'll probably want to send the processed image to the model, predict steering angle,
            # and then send motor commands. 

            # TESTING display both frames
            cv.imshow("Video", frame)
            cv.imshow("Processed", detectedLines)

########## Main ##########
def main():
    print("\nmain is running")

    vehicle = AVI()
    
    vehicle.Drive()

if __name__ == "__main__":
    main()
    
    # sys.exit(main())  <-- not sure why but the camera code didn't work with this.

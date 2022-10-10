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
#
#============================================================

import sys 
import numpy as np
import cv2 as cv
from Camera import *

print("python version: ",sys.version)
print("numpy version: ",np.__version__)

# Camera driver code. Will need to be reworked for our final implementation
def getCamera(src = 0):

        # start the camera
        videoCapture = Camera(src).startCamera()

        while True:
            # Stop if the user presses "q" TODO: we need some other way to stop this.
            if (cv.waitKey(1) == ord("q")) or videoCapture.stopped:
                videoCapture.stopCamera()
                break

            frame = videoCapture.frame

            cv.imshow("Video", frame)

def main():
    print("\nmain is running")

    # comment this out if you want to test other stuff.
    getCamera(0)

if __name__ == "__main__":
    main()
    
    # sys.exit(main())  <-- not sure why but the camera code didn't work with this.

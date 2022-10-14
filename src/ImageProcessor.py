#============================================================
#
#                         HTTP 418
#               CSE 4316/4317 - Senior Design
#            The University of Texas at Arlington
#    Dylan Bryce, Biraj GC, Preston Mann, Isabel Metevier
#
#============================================================
#
# File: ImageProcessor.py
#
# Brief: This file contains all of the classes related to the
#        Image Processing Layer
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 10-10-2022 | Bryce, D     | Initial Release
#
#============================================================

import cv2 as cv
import numpy as np

## @brief This class does the image processing.
class ImageProcessor(object):

    ## @brief Default constructor
    def __init__(self):
        pass

    ## @brief Processes an image to detect the lines of tape.
    ## @param image frame: an image to be processed
    ## @return image lines: a grayscale, edge-detected image
    def extractLines(self, frame): 
        into_hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    
        L_limit = np.array([0,50,50],np.uint8) # setting the orange lower limit
        U_limit = np.array([30,255,255],np.uint8) # setting the orange upper limit
 
        o_mask = cv.inRange(into_hsv,L_limit,U_limit)
        orange = cv.bitwise_and(frame,frame,mask=o_mask)
    
        lines = cv.Canny(o_mask, 200, 400)
    
        # this is not needed, this writes the processed images to a directory and we just need the lines.
        cv.imwrite("lab_test_hsv.png",into_hsv) 
        cv.imwrite("lab_test_mask.png",o_mask)
        cv.imwrite("lab_test_orange_detection.png",orange) 
        cv.imwrite("lab_test_line_detected.png",lines) 
    
        return lines 
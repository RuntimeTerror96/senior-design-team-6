#============================================================
#
#                         HTTP 418
#               CSE 4316/4317 - Senior Design
#            The University of Texas at Arlington
#    Dylan Bryce, Biraj GC, Preston Mann, Isabel Metevier
#
#------------------------------------------------------------
#
# File: doxygen-example.py
#
# Brief: This file serves as an example of documenting Python
#        source code with Doxygen
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 09-10-2022 | Mann, P.    | Initial Release
#
#============================================================



import cv2
import numpy as np
#https://www.geeksforgeeks.org/real-time-object-color-detection-using-opencv/

#this code example is supposed to track the blue color in a image
#the goal is for it to be more robust line detector than extract lines example 
#however so far its about the same as the other method 

def detect_lines(frame): 
    into_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    L_limit=np.array([98,50,50]) # setting the blue lower limit
    U_limit=np.array([139,255,255]) # setting the blue upper limit
        
 
    b_mask=cv2.inRange(into_hsv,L_limit,U_limit)
    blue=cv2.bitwise_and(frame,frame,mask=b_mask)
    lines = cv2.Canny(b_mask, 200, 400)
    
    cv2.imwrite("open_cv_detect_lines.png",lines)
    
    return lines 

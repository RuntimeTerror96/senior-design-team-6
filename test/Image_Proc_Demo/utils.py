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
# 09-10-2022 | Mann, P.     | Initial Release
# 09-14-2022 | Mann, P.     | Added functions 
#============================================================



import cv2
import numpy as np
import sys 
import skimage
import skimage.io as io
from skimage import data
from skimage.color import rgb2hsv,rgb2gray
from skimage import feature
from skimage.filters import threshold_otsu
from skimage import feature

#https://www.geeksforgeeks.org/real-time-object-color-detection-using-opencv/

#this code example is supposed to track the blue color in a image
#the goal is for it to be more robust line detector than extract lines example 
#however so far its about the same as the other method 

#///////////////////////////////////////////////////////////////////////

def detect_lines(frame): 
    into_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    L_limit=np.array([0,50,50],np.uint8) # setting the orange lower limit
    U_limit=np.array([30,255,255],np.uint8) # setting the orange upper limit
 
    o_mask=cv2.inRange(into_hsv,L_limit,U_limit)
    orange=cv2.bitwise_and(frame,frame,mask=o_mask)
    
    lines = cv2.Canny(o_mask, 200, 400)
    
    cv2.imwrite("lab_test_hsv.png",into_hsv) 
    cv2.imwrite("lab_test_mask.png",o_mask)
    cv2.imwrite("lab_test_orange_detection.png",orange) 
    cv2.imwrite("lab_test_line_detected.png",lines) 
    
    return lines 
#this is the current method being used to detect lines
#////////////////////////////////////////////////////////////////////////////////////


def detect_lines_old(frame): 
    into_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #blue_lower=np.array([100,150,0],np.uint8)
    #blue_upper=np.array([140,255,255],np.uint8) 
    
    L_limit=np.array([98,50,50]) # setting the blue lower limit
    U_limit=np.array([139,255,255]) # setting the blue upper limit
    #RGB in open cv is BGR  
 
    b_mask=cv2.inRange(into_hsv,L_limit,U_limit)
    blue=cv2.bitwise_and(frame,frame,mask=b_mask)
    lines = cv2.Canny(b_mask, 200, 400)
    cv2.imwrite("open_cv_test_hsv.png",into_hsv) 
    cv2.imwrite("open_cv_detect_lines.png",lines)
    
    return lines 



#this is the demo function that I made first 
# this is just a basic overview on how to do image processing 
# we are no longer using this lib we are using open cv now 
def extract_lines():
    rgb_img = io.imread("test_pic.png")
    hsv_img = rgb2hsv(rgb_img)
    gray_img = rgb2gray(rgb_img) 
    
    #hue_img = hsv_img[:, :, 0]
    #value_img = hsv_img[:, :, 2]
    #this is how you get the hue or value for HSV images 
    # rgb2gray converts image to gray scale
    #more on color can be read here 
    # https://dillhoffaj.utasites.cloud/posts/color/ 
    io.imsave("rgb_to_hsv_example.png", hsv_img)
    io.imsave("rgb2gray.png",gray_img)
    
    # we want to threshold the hsv img so that we can filter some junk out 
    # the goal is to just have 2 lines then we can do a edge detection to 
    # find these lines 
    thresh = threshold_otsu(rgb2gray(hsv_img))
    binary = rgb2gray(hsv_img) > thresh
    io.imsave("binary_of_threshold.png",binary)
    #here we can do more stuff to the image to get a better detection 
    edge = feature.canny(binary)
    io.imsave("edge_example.png",edge)


def extract_lines_v2(frame):

    rgb_img = frame/255
    hsv_img = rgb2hsv(rgb_img)
    gray_img = rgb2gray(rgb_img) 
    
    hsv_img[:, :, 0] -= 0.1
    #hue_img = hsv_img[:, :, 0]
    #value_img = hsv_img[:, :, 2]
    #this is how you get the hue or value for HSV images
    # rgb2gray converts image to gray scale
    #more on color can be read here
    # https://dillhoffaj.utasites.cloud/posts/color/
    io.imsave("rgb_to_hsv_lab_test.png", hsv_img)
    io.imsave("rgb2gray_lab_test.png",gray_img)

    # we want to threshold the hsv img so that we can filter some junk out
    # the goal is to just have 2 lines then we can do a edge detection to
    # find these lines
    thresh = threshold_otsu(rgb2gray(hsv_img))
    binary = rgb2gray(hsv_img) > thresh
    io.imsave("binary_of_threshold_lab_test.png",binary)
    #here we can do more stuff to the image to get a better detection
    edge = feature.canny(binary)
    io.imsave("edge_example_lab_test.png",edge)





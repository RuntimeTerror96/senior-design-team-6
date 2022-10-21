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
# 01-01-2022 | Mann, P.    | Initial Release
#
#============================================================

# The example below is a driver which outlines how to do image proc. in python
import numpy as np
import sys 
import cv2
# import skimage
# import skimage.io as io
# from skimage import data
# from skimage.color import rgb2hsv,rgb2gray
# from skimage import feature
# from skimage.filters import threshold_otsu
# from skimage import feature
from utils import detect_lines
# from utils import extract_lines_v2
# from utils import extract_lines
print("python version: ",sys.version)
print("numpy version: ",np.__version__)
# print("skiamge version: ",skimage.__version__)

# driver code

def main():
    #///////////////////////////////////////////////////////////////////////////
    #extract_lines()
    #this is the idea I have for line detection un comment this code for the demo 
    # this method was moved to utils 
    #////////////////////////////////////////////////////////////////////////////
    
    
    #///////////////////////////////////////
    #rgb_img = io.imread("test_pic.png")
    #using_open_cv = detect_lines(rgb_img)
    #rgb_img2 = io.imread("IMG_2773.jpg")
    #using_open_cv - detect_lines(rgb_img2)
    #//////////////////////////////////////
    #this is for testing open cv method of line detection in the util detect lines function 

    rgb_img_2 = cv2.imread("IMG_2774.png")
    #extract_lines_v2(rgb_img_2) 
    blue_mask = detect_lines(rgb_img_2)
    #current way of detecting lines using open CV 
if __name__ == "__main__":
    main()


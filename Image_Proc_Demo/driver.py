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
import skimage
import skimage.io as io
from skimage import data
from skimage.color import rgb2hsv,rgb2gray
from skimage import feature
from skimage.filters import threshold_otsu
from skimage import feature
from utils import detect_lines
print("python version: ",sys.version)
print("numpy version: ",np.__version__)
print("skiamge version: ",skimage.__version__)

# driver code

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

def main():
    extract_lines()
    #this is the idea I have for line detection 
    #TODO add more functions for image processing     
    rgb_img = io.imread("test_pic.png")
    using_open_cv = detect_lines(rgb_img)

if __name__ == "__main__":
    main()


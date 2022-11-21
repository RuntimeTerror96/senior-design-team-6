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
# Brief: This file is our model to run to test code it will run any test we need  
#        Anythong can go in here when you make a branch and we wont worry about merge conflicts 
#        
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 09-26-2022 | Mann, P.    | Initial Release
# 10-12-2022 " Mann, P.     | testing model class 
# 10-21-2022 " Mann, P.     | removed the main and added a img preprocess test
#
#============================================================

import sys 
import numpy as np
from model import Model_obj
print("python version: ",sys.version)
print("numpy version: ",np.__version__)
import cv2

def my_imread(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def img_preprocess(frame):
    into_hsv =cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)

    cv2.imwrite("into_hsv.png",into_hsv)
    
    L_limit=np.array([88,25,208],np.uint8) # setting the orange lower limit
    U_limit=np.array([136,255,255],np.uint8) # setting the orange upper limit

    o_mask=cv2.inRange(into_hsv,L_limit,U_limit)
    orange=cv2.bitwise_and(frame,frame,mask=o_mask)

    lines = cv2.Canny(o_mask, 200, 400)

    cv2.imwrite("lab_test_hsv.png",into_hsv)
    cv2.imwrite("lab_test_mask.png",o_mask)
    cv2.imwrite("lab_test_orange_detection.png",orange)
    cv2.imwrite("lab_test_line_detected.png",lines)


    orange_200 = cv2.resize(orange, (200,66))
    
    cv2.imwrite("lab_test_orange_detection_norm.png",orange_200)
    return orange
#path = "/home/senior-design/Documents/data/9-21 Dylan-3/IMG__1692_0_1.png"
#img = my_imread(path)

#mask = img_preprocess(img)


def main():
    print("\ntest is running")
    test = Model_obj()
#    test.load("test_model.keras")
    test.make_model()
    test.get_model_summary()
    test.train_model()
    test.model_save("test_model_11-19.keras")


if __name__ == "__main__":
    sys.exit(main())

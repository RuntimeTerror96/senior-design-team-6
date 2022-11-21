import cv2
import os 
import fnmatch
import random
import numpy as np

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
# Brief: This file that has util functions needed for the model class
#        #
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 10-12-2022 | Mann, P.    | Initial Release
# 10-13-2022 | Mann, P.     | minor changes 
#
#============================================================



def my_imread(image_path):
    image = cv2.imread(image_path)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image
def get_data():
    data_dir = '/home/senior-design/Documents/data2/'
    file_list = os.listdir(data_dir)
    image_paths = []
    targets = []
    count = 1
    pattern = "*.png"
    for filename in file_list:
        if fnmatch.fnmatch(filename, pattern):
            image_paths.append(os.path.join(data_dir,filename))
            parse_ = filename.split("_")
            
            #print(parse_)
            parse_dot = parse_[3].split(".")
            turn = parse_dot[0]
            targets.append(int(turn))
            #print(turn)
            #IMG__122_-1_1.png
    return image_paths,targets
def image_data_generator(image_paths, targets, batch_size, is_training):
    while True:
        batch_images = []
        batch_targets = []

        for i in range(batch_size):
            random_index = random.randint(0, len(image_paths) - 1)
            image_path = image_paths[random_index]
            image = my_imread(image_paths[random_index])
            target = targets[random_index]

            image = test_process(image)
            batch_images.append(image)
            batch_targets.append(target)

        yield( np.asarray(batch_images), np.asarray(batch_targets))

def img_preprocess(frame):
    into_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    
    L_limit = np.array([88,25,208],np.uint8) # setting the orange lower limit
    U_limit = np.array([136,255,255],np.uint8) # setting the orange upper limit
 
    o_mask=cv2.inRange(into_hsv,L_limit,U_limit)
    orange=cv2.bitwise_and(frame,frame,mask=o_mask)

    lines = cv2.Canny(o_mask, 200, 400)

    #cv2.imwrite("lab_test_hsv.png",into_hsv)
    #cv2.imwrite("lab_test_mask.png",o_mask)
    #cv2.imwrite("lab_test_orange_detection.png",orange)
    #cv2.imwrite("lab_test_line_detected.png",lines)


    orange = cv2.resize(orange, (200,66))
    orange = orange / 255
    
    cv2.imwrite("lab_test_hsv.png",into_hsv)
    return orange

def test_process(image):
    height, _, _ = image.shape
   # image = image[int(height/2):,:,:]  # remove top half of the image, as it is not relavant for lane followingUUimage = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)  # Nvidia model said it is best to use YUV color space
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)  # Nvidia model said it is best to use YUV color space
    image = cv2.resize(image, (200,66)) # input image size (200,66) Nvidia model
    image = image / 255 # normalizing, the processed image becomes black for some reason.  do we need this?
   # cv2.imwrite("test.png",image)
    return image


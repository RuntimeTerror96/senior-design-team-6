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
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image
def get_data():
    data_dir = '/home/senior-design/Documents/data/9-20 Biraj-2'
    file_list = os.listdir(data_dir)

    image_paths = []
    targets = []

    pattern = "*.png"
    for filename in file_list:
        if fnmatch.fnmatch(filename, pattern):
            image_paths.append(os.path.join(data_dir,filename))
            turn_S = filename[-6:-4]
            if turn_S == '_1':
                turn = 1
            if turn_S == '_0':
                turn = 0
            if turn_S == '-1':
                turn = 2
            targets.append(turn)
            #IMG__122_-1_1.png
    data_dir = '/home/senior-design/Documents/data/9-21 Dylan-1'
    file_list = os.listdir(data_dir)
    for filename in file_list:
        if fnmatch.fnmatch(filename, pattern):
            image_paths.append(os.path.join(data_dir,filename))
            turn_S = filename[-6:-4]
            if turn_S == '_1':
                turn = 1
            if turn_S == '_0':
                turn = 0
            if turn_S == '-1':
                turn = 2
            targets.append(turn)
    data_dir = '/home/senior-design/Documents/data/9-21 Dylan-2'
    file_list = os.listdir(data_dir)
    for filename in file_list:
        if fnmatch.fnmatch(filename, pattern):
            image_paths.append(os.path.join(data_dir,filename))
            turn_S = filename[-6:-4]
            if turn_S == '_1':
                turn = 1
            if turn_S == '_0':
                turn = 0
            if turn_S == '-1':
                turn = 2
            targets.append(turn)
    data_dir = '/home/senior-design/Documents/data/9-21 Dylan-3'
    file_list = os.listdir(data_dir)
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

            image = img_preprocess(image)
            batch_images.append(image)
            batch_targets.append(target)

        yield( np.asarray(batch_images), np.asarray(batch_targets))

def img_preprocess(frame):
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


    orange = cv2.resize(orange, (200,66))
    orange = orange / 255
    return orange


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
# Brief: This file is our model for path finding will be 
#        it will be a class where you can make a model object
#        the object will have the follwing methods 
#        Train model,Load model,Print model summary
#        model predict
# 
#        
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 09-26-2022 | Mann, P.    | Initial Release
# 10-07-2022 ' mann, P/    | added the data proc. 
# 10-1102922 | mann, P.     | worked on code base
#
#============================================================

import os
import random
import fnmatch

import numpy as np


import tensorflow as tf
import keras
from keras.models import Sequential  # V2 is tensorflow.keras.xxxx, V1 is keras.xxx
from keras.layers import Conv2D, MaxPool2D, Dropout, Flatten, Dense
from keras.optimizers import Adam
from keras.models import load_model


from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

import cv2
from imgaug import augmenters as img_aug
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from tensorflow.keras import layers

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
                print("test")
            targets.append(turn)
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
              
            image = img_preprocess(image)
            batch_images.append(image)
            batch_targets.append(target)
            
        yield( np.asarray(batch_images), np.asarray(batch_targets))
            
def img_preprocess(frame):
    
    #image = cv2.GaussianBlur(image, (3,3), 0)
   # image = cv2.resize(image, (200,66)) 
    #image = image / 255     

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

def model_path():
    #TODO 
    # we can make H and W define here or passed as args 
    #model_path as a object and put methdos to do ever thing we need
    # for now its one fucntion but later I will change it to a object
    height=150 
    width = 150
    input_shape=(200,66,3)
    

    ncol = 2
    nrow = 2        
    
    image_paths , targets = get_data()
    X_train, X_valid, y_train, y_valid = train_test_split( image_paths, targets, test_size=0.2)

    # this is the task for input layer I need to make sure the shape of my data is correct for trianing 
    #after I get it all procesed and loaded 
    model = keras.Sequential(    [
        keras.Input(shape=input_shape)
    ])
    
    #output layer task and cnn/dense layer task will take place here 
    #I wrote the min amount of layers now we need to fine tune it and make it robust for training 
    

    model.add(Conv2D(24, (5, 5), strides=(2, 2), activation='elu')) 
    model.add(Conv2D(36, (5, 5), strides=(2, 2), activation='elu')) 
    model.add(Conv2D(48, (5, 5), strides=(2, 2), activation='elu')) 
    model.add(Conv2D(64, (3, 3), activation='elu')) 
    model.add(Conv2D(64, (3, 3), activation='elu')) 
    
    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))

    model.add(layers.Dense(3))
    

    X_train_batch, y_train_batch = next(image_data_generator(X_train, y_train, nrow, True))   
    
    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


    history = model.fit(image_data_generator( X_train, y_train, batch_size=1, is_training=True),
                              steps_per_epoch=300,
                              epochs=10
                              )
    model.save('model.keras')
    return model

def create_image_plots():
    test_path = "/home/senior-design/Documents/data/9-20 Biraj-2/IMG__4262_1_1.png"
    img_RGB = my_imread(test_path)
    img_Proc = img_preprocess(img_RGB)
    plt.subplot(1, 2, 1)
    plt.imshow(img_RGB)
    plt.subplot(1, 2, 2)
    plt.imshow(img_Proc)
    plt.show()
#create_image_plots()
newModel = model_path()
newModel.summary()


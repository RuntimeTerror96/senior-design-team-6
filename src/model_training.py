import os
import random
import fnmatch

import numpy as np

import tensorflow as tf
from tensorflow import keras 
from keras.models import Sequential  # V2 is tensorflow.keras.xxxx, V1 is keras.xxx
from keras.layers import Conv2D, MaxPool2D, Dropout, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from keras.models import load_model


from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

import cv2 as cv
import cv2
from imgaug import augmenters as img_aug
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from tensorflow.keras import layers
from load_data_set import get_data
from load_data_set import image_data_generator


def countX(lst, x):
    count = 0
    for ele in lst:
        if (ele == x):
            count = count + 1
    return count

## @brief This class makes a model object that can be trained. It can also load a trained model and use it for predictions
class Model_obj:
    def __init__(self):
        self.model = tf.keras.Model()
    ## @brief Makes a new model for training.
    ## @param Model_obj self - The object that the method using this will set the self.model to the model the methond makes
    ## @return void 
    def make_model(self):
        height=200
        width = 66
        input_shape=(height,width,3)

        model = keras.Sequential(    [
            keras.Input(shape=input_shape)
        ])

        model.add(Conv2D(24, (5, 5), strides=(2, 2), activation='elu'))
        model.add(Conv2D(36, (5, 5), strides=(2, 2), activation='elu'))
        model.add(Conv2D(48, (5, 5), strides=(2, 2), activation='elu'))
        model.add(Conv2D(64, (3, 3), activation='elu'))
        model.add(Conv2D(64, (3, 3), activation='elu'))

        model.add(Flatten())
        model.add(Dense(100, activation='elu'))
        model.add(Dense(50, activation='elu'))
        model.add(Dense(10, activation='elu'))

        model.add(layers.Dense(1))
    
        model.compile(optimizer='adam',
              loss="mse",
              metrics=['accuracy'])
        self.model = model
    ## @brief Trains a model.
    ## @param Model_obj self - The object that the method using. this will train the self.model
    ## @return void 
    
    def train_model(self):
        image_paths , targets = get_data()
        
       # print("amount of -1s: ",countX(targets,2))
       # print("amount of 0s: ",countX(targets,0))
       # print("amount of 1s: ",countX(targets,1))

        size_of_data = len(image_paths)-1
        print("size of Traing data ",len(image_paths))

        X_train, X_valid, y_train, y_valid = train_test_split( image_paths, targets, test_size=0.2)
        X_train_batch, y_train_batch = next(image_data_generator(X_train, y_train, 2, True))

        self.model.fit(image_data_generator( X_train, y_train, batch_size=1, is_training=True),
                             steps_per_epoch=size_of_data,
                              epochs=10
                              )
    ## @brief Getter for model summary.
    ## @param Model_obj self - The object that the method using.     
    ## @return void 
 
    def get_model_summary(self):
        self.model.summary()

    ## @brief saves the self.model as a file.
    ## @param Model_obj self - The object that the method using.     
    ## @param string file_name - name of the file to save the model to should be a .keras   
    ## @return void 
    def model_save(self,file_name):
        self.model.save(file_name)

    def load(self,path):
        self.model = keras.models.load_model(path)
    
    
    def model_calc_anlge(self,frame):
        theta = self.model.predict(frame)
        return theta

    def convert_model_to_lite(self, filename = "C:/Users/biraj/Documents/GitHub/senior-design-team-6/src/tf_lite_model.tflite"):
        TF_LITE_FILE_NAME = filename
        tf_lite_converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        tflite_model = tf_lite_converter.convert()
        open(TF_LITE_FILE_NAME, "wb").write(tflite_model)
        return tflite_model


    def model_calc_angle(self,frame):
        frame_convert =  np.array(frame, dtype=np.float32)
        self.model_interpreter.set_tensor(self.input_details[0]['index'], frame_convert)
        self.model_interpreter.invoke()
        predict = self.model_interpreter.get_tensor(self.output_details[0]['index'])
        return predict[0]
    
    def loadTFliteModel(self, path):
        self.model_interpreter  =  tf.lite.Interpreter(model_path=path)
        self.input_details = self.model_interpreter.get_input_details()
        self.output_details = self.model_interpreter.get_output_details()
        # self.model_interpreter.resize_tensor_input(self.input_details[0]['index'], (1, 200, 66, 3))
        self.model_interpreter.allocate_tensors()
        self.input_details = self.model_interpreter.get_input_details()
        print("Input Shape:", self.input_details[0]['shape'])
        print("Output Shape:", self.output_details[0]['shape'])

def frameToHSV(frame):
        height, _, _ = frame.shape
        frame = frame[int(height/2):,:,:]  # remove top half of the image, as it is not relevant for lane following
        frame = cv.cvtColor(frame, cv.COLOR_RGB2YUV)  # Nvidia model said it is best to use YUV color space
        frame = cv.GaussianBlur(frame, (3,3), 0)
        frame = cv.resize(frame, (66, 200)) # input image size (200,66) Nvidia model
        frame = frame / 255 # normalizing
        print(frame.shape)
        return frame

def test():
    # load the model
    model = Model_obj()
    model.load("C:/Users/biraj/Documents/GitHub/senior-design-team-6/src/test_model.keras")

    #load the frame
    frame = cv.imread("C:/Users/biraj/Documents/GitHub/senior-design-team-6/src/TEST_IMG.png")
    #convert the frame
    frame = frameToHSV(frame)
    arr = np.array([frame])
    print(arr.shape) # required shape is [1, 200, 66, 3] it is important the the frame must be this  

    # 'Regular Using Just TensorFlow'
    print(model.model_calc_anlge(arr))
    # 'Using Just TensorFlow Lite'
    #load the lite model
    model.loadTFliteModel("C:/Users/biraj/Documents/GitHub/senior-design-team-6/src/tf_lite_model.tflite")
    print(model.model_calc_angle(arr))

if __name__ == '__main__':
    test()
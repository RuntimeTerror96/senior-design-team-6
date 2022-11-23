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
def train_model(self):

    def get_model_summary(self):
        self.model.summary()

    ## @brief saves the self.model as a file.
    ## @param Model_obj self - The object that the method using.     
    ## @param string file_name - name of the file to save the model to should be a .keras   
class model_save:
    def __init__(self):
        self.model = tf.keras.Model()

    def load(self,path):
        self.model = keras.models.load_model(path)


    def model_calc_anlge(self,frame):
        theta = self.model.predict(frame)
        return theta

    def convert_model_to_lite(self,filename):
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
    
    path = "/home/senior-design/Documents/senior-design-team-6/src/models/loss49.keras"
    model = model_save()
    model.load(path)

    #load the frame
    #frame = cv.imread("C:/Users/biraj/Documents/GitHub/senior-design-team-6/src/TEST_IMG.png")
    #convert the frame
   # frame = frameToHSV(frame)
   # arr = np.array([frame])
   # print(arr.shape) # required shape is [1, 200, 66, 3] it is important the the frame must be this  

    # 'Regular Using Just TensorFlow'
 #   print(model.model_calc_anlge(arr))
    # 'Using Just TensorFlow Lite'
    #load the lite model
    model.convert_model_to_lite("loss_49test.tflite")
  #  print(model.model_calc_angle(arr))

if __name__ == '__main__':
    test()

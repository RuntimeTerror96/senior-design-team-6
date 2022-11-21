import sys

import numpy as np
import tflite_runtime.interpreter as tflite


class TFlite_model:
    def __init__(self, path = None):
        if path == None:
            self.model_loaded = False
            self.model_interpreter  =  None
            self.input_details = None
            self.output_details = None
        else:
            self.model_interpreter  =  tflite.Interpreter(model_path=path)
            self.input_details = self.model_interpreter.get_input_details()
            self.output_details = self.model_interpreter.get_output_details()
            self.model_interpreter.allocate_tensors()
            self.model_loaded = True 

    def model_calc_angle(self,frame):
        if self.model_loaded:
            frame_convert =  np.array(frame, dtype=np.float32)
            self.model_interpreter.set_tensor(self.input_details[0]['index'], frame_convert)
            self.model_interpreter.invoke()
            predict = self.model_interpreter.get_tensor(self.output_details[0]['index'])
            return predict[0]
        else:
            print("Model has not been loaded to object")
    
    def loadTFliteModel(self, path):
        self.model_interpreter  =  tflite.Interpreter(model_path=path)
        self.input_details = self.model_interpreter.get_input_details()
        self.output_details = self.model_interpreter.get_output_details()
        self.model_interpreter.allocate_tensors()
        self.model_loaded = True 

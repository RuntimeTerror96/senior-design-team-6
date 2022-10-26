#============================================================
#
#                         HTTP 418
#               CSE 4316/4317 - Senior Design
#            The University of Texas at Arlington
#    Dylan Bryce, Biraj GC, Preston Mann, Isabel Metevier
#
#============================================================
#
# File: Reconcilliator.py
#
# Brief: <description>
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 10-16-2022 | GC, B.       | <description>
#
#============================================================

import numpy as np

## @brief This class converts the output from two difrrent NN Model and makes decsions.
## This class contains all three sub modules as functions of Model Reconcilliator layer.  
## This class shall be used in main function to pass in the models, pass in the inputs, make decisions and pass the outputs.
class Reconcilliator:

    ## @brief Initialize the Reconcilliator object using NN models.
    ## @param Keras.Model pathFindingModel - the model is used to compute directions to obtain steering angle for the vechicle.
    ## @param Keras.Model objDetectionModel - the model is used to detect objects and signs. #TODO: after completing Obj detection Layer 
    def __init__(self, pathFindingModel, objDetectionModel = None) -> None:
        self.pathFindingModel  =  pathFindingModel
        self.objDetectionModel =  objDetectionModel
        

    ## @brief Uses the Neural Network to compute the data for a given frame.
    ## @param type nnInputData - A preprocessed frame that is used to compute steering angle by NN pathFinding model.

    def inputManager(self, nnInputData):
        steeringAngle = self.pathFindingModel.predict(nnInputData)[0]
        #TODO
        #objDetection =  self.pathFindingModel.predict(nnInputData)[0]
        #return steeringAngle, objDetection
        return steeringAngle

    ## @brief Evaluates output from pathfinding model and object recognition model and generates an arra
    ## @param type nnInputData - A preprocessed frame that is used to compute steering angle by NN pathFinding model.
    def decisionModule(self):
        #nnOutput = self.inputManager()
        #return nnOutput
        #Todo: IMPLEMENT DECISION MODULE AFTER COMPLETION OF OBJECT RECOGNIION
        pass
    
    ## @brief Calls input manager, decision module function and retunrs output ready to be fed to the car
    ## @param type nnInputData - A preprocessed frame that is used to compute steering angle by NN pathFinding model.
    def outputGenerator(self, nnInputData):
        #Todo: IMPLEMENT Output manager Module AFTER COMPLETION OF OBJECT RECOGNIION
        #This module should take in the output from decision module and lay the outputs in form of array to be pushed 
        self.inputManager(nnInputData)
    
    


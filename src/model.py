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
#
#============================================================


from tensorflow.keras import layers

def model_path():
    #TODO 
    # we can make H and W define here or passed as args 
    #model_path as a object and put methdos to do ever thing we need
    # for now its one fucntion but later I will change it to a object
    height=150 
    width = 150
    input_shape=(height,width,3)
    

    # this is the task for input layer I need to make sure the shape of my data is correct for trianing 
    #after I get it all procesed and loaded 
    model = keras.Sequential(    [
        keras.Input(shape=input_shape)
    ])
    
    #output layer task and cnn/dense layer task will take place here 
    #I wrote the min amount of layers now we need to fine tune it and make it robust for training 
    model.add(layers.Conv2D(24, (5, 5), strides=(2, 2), activation='elu')) 
    model.add(layers.Flatten())
    model.add(layers.Dense(100, activation='elu'))
    model.add(layers.Dense(1)) 
    
    model.compile(loss='mse', optimizer='adam')
    
    return model


newModel = model_path()
newModel.summary()



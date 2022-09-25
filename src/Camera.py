#============================================================
#
#                         HTTP 418
#               CSE 4316/4317 - Senior Design
#            The University of Texas at Arlington
#    Dylan Bryce, Biraj GC, Preston Mann, Isabel Metevier
#
#============================================================
#
# File: Camera.py
#
# Brief: This file contains all of the classes related to the
#        Image Processing Layer
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 09-25-2022 | Bryce, D     | Initial Release
#
#============================================================

## @brief This class contains driver code for interfacing with the camera.
## Camera is a singleton class so only one istance of a Camera object
## can be created. This class contains all needed functions to connect
## to and interface with the camera.
class Camera:

    ## @brief Default constructor enforcing the singleton pattern.
    ## If a Camera object already exists, this function returns a reference
    ## to that object. Else, it creates a new Camera object.
    ## @param Camera cls - The object being created (leave this blank when calling the function)
    ## @return Camera cls - A Camera object
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Camera, cls).__new__(cls)
        return cls.instance

    

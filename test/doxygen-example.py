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
# Brief: This file serves as an example of documenting Python
#        source code with Doxygen
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 08-06-2022 | Bryce, D.    | Initial Release
#
#============================================================

# The example below outlines how to document a python class
# and its members using Doxygen tags. The example starts at
# line 26.

## @brief This class does nothing.
class MyClass:
    
    ## @brief Default Constructor
    def __init__(self):
        pass
    
    ## @brief Prints out a name passed by caller and returns the meaning of life.
    ## @param MyClass self - The object that the method is being called upon
    ## @param string name - The name to be printed
    ## @return int aVar - The meaning of life
    def myMethod(self, name):
        print("Hello, my name is " + name)
        aVar = 42
        return aVar

# driver code
def main():

    anObject = MyClass()
    ret = anObject.myMethod("Dylan")
    print(ret)

if __name__ == "__main__":
    main()
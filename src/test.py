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
# Brief: This file is our model to run to test code it will run any test we need  
#        Anythong can go in here when you make a branch and we wont worry about merge conflicts 
#        
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 09-26-2022 | Mann, P.    | Initial Release
# 10-12-2022 " Mann, P.     | testing model class 
#
#============================================================

import sys 
import numpy as np
from model import Model_obj
print("python version: ",sys.version)
print("numpy version: ",np.__version__)


def main():
    print("\ntest is running")
    test = Model_obj()
    test.make_model()
    test.get_model_summary()
    test.train_model()
    test.model_save("test_model.keras")


if __name__ == "__main__":
    sys.exit(main())


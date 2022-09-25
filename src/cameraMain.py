from Camera import *
import time

def main():
    cam = Camera()

    cam.openCamera()

    cam.startCamera()
    #cam.captureData()

    time.sleep(10)
    cam.closeCamera()

if __name__ == "__main__":
    main()
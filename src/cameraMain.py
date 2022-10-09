from Camera import *
import cv2 as cv

def getCamera(src = 0):

        # start the camera
        videoCapture = Camera(src).startCamera()

        while True:
            # Stop if the user presses "q" TODO: we need some other way to stop this.
            if (cv.waitKey(1) == ord("q")) or videoCapture.stopped:
                videoCapture.stopCamera()
                break

            frame = videoCapture.frame

            cv.imshow("Video", frame)

def main():
    getCamera(0)

if __name__ == "__main__":
    main()
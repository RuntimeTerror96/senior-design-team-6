#============================================================
#
#                         HTTP 418
#               CSE 4316/4317 - Senior Design
#            The University of Texas at Arlington
#    Dylan Bryce, Biraj GC, Preston Mann, Isabel Metevier
#
#============================================================
#
# File: ImageProcessor.py
#
# Brief: This file contains all of the classes related to the
#        Image Processing Layer
#
# Revision History:
# Date       | Engineer     | Description
# -----------|--------------|--------------------------------
# 10-10-2022 | Bryce, D     | Initial Release
#
#============================================================

import os
import time
import cv2 as cv
import numpy as np
import math

## @brief This class does the image processing.
class ImageProcessor(object):

    ## @brief Default constructor
    ## @param bool showImages - flag for showing images (i.e. during testing or demo)
    ## @param bool debug - flag for logging debug info to the console
    def __init__(self, showImages=False, debug=False):
        self.showImages = showImages
        self.debug = debug

    ## @brief Processes an image to detect the lines of tape.
    ## @param image frame: an image to be processed
    ## @return image lines: a grayscale, edge-detected image
    def extractLines(self, frame):
        if self.showImages == True:
            cv.imshow("Original", frame)

        into_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
        L_limit = np.array([88,25,208],np.uint8) # setting the orange lower limit
        U_limit = np.array([136,255,255],np.uint8) # setting the orange upper limit
 
        o_mask = cv.inRange(into_hsv,L_limit,U_limit)
        orange = cv.bitwise_and(frame,frame,mask=o_mask)
    
        lines = cv.Canny(o_mask, 200, 400)
    
        masked = self.maskImage(lines)

        if self.showImages == True:
            cv.imshow("Lines", masked)

        return masked

    # TODO: documentation
    def maskImage(self, frame):
        height, width = frame.shape
        mask = np.zeros_like(frame)

        rect = np.array([[(0, height * 1 / 2), (width, height * 1 / 2), (width, height), (0, height), ]], np.int32)

        cv.fillPoly(mask, rect, 255)

        masked = cv.bitwise_and(frame, mask)

        return masked

    # TODO: documentation
    # NOTE: will return "None" on bad image, make sure you have an "if not none" wrapper when calling this
    # NOTE: minThreshold, minLineLength, and maxLineGap may require tuning
    def getLineSegments(self, edges):
        rho = 1
        angle = np.pi / 180
        minThreshold = 10

        segments = cv.HoughLinesP(edges, rho, angle, minThreshold, np.array([]), minLineLength=10, maxLineGap=4)

        if self.debug == True and segments is not None:
            for segment in segments:
                print('detected line segment:')
                print("%s of length %s" % (segment, lengthOfSegments(segment[0])))

        return segments

####### Test functions #######
def lengthOfSegments(line):
    x1, y1, x2, y2 = line
    return math.sqrt((x2-x1) ** 2 + (y2 - y1) ** 2)

def displayLaneLines(frame, lines, lineColor=(0, 255, 0), lineWidth=10):
    lineImage = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv.line(lineImage, (x1, y1), (x2, y2), lineColor, lineWidth)

    lineImage = cv.addWeighted(frame, 0.8, lineImage, 1, 1)
    return lineImage

# Combines all line segments into one or two lines
# if all slopes are < 0: only left lane detected
# if all slopes are > 0: only right lane detected
def avgSlopeIntercept(frame, lineSegs):
    lanes = []

    if lineSegs is None:
        return lanes

    height, width, _ = frame.shape
    leftFit = []
    rightFit = []

    boundary = 1/3
    leftBoundary = width * (1 - boundary)   # left lane should be on left 2/3 of the screen
    rightBoundary = width * boundary        # right lane should be on right 2/3 of the screen

    for segment in lineSegs:

        for x1, y1, x2, y2 in segment:

            # skip vertical line segment
            if x1 == x2:
                continue

            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]

            if slope < 0:
                if x1 < leftBoundary and x2 < leftBoundary:
                    leftFit.append((slope, intercept))
            else:
                if x2 > rightBoundary and x2 > rightBoundary:
                    rightFit.append((slope, intercept))

    leftFitAvg = np.average(leftFit, axis=0)
    if len(leftFit) > 5:
        lanes.append(makePoints(frame, leftFitAvg))

    rightFitAvg = np.average(rightFit, axis=0)
    if len(rightFit) > 5:
        lanes.append(makePoints(frame, rightFitAvg))

    return lanes


def makePoints(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line

    y1 = height
    y2 = int(y1 * 1 / 2)

    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))

    return [[x1, y1, x2, y2]]

def calcSteeringAng(frame, lanes):

    # No lines detected
    if len(lanes) == 0:
        return -90

    height, width, _ = frame.shape

    # one line detected
    if len(lanes) == 1:
        x1, _, x2, _ = lanes[0][0]
        xOffset = x2 - x1
    else:
        _, _, leftX2, _ = lanes[0][0]
        _, _, rightX2, _ = lanes[1][0]
        camOffset = 0.02    # we will probably need to adjust this... 0.0 = pointing dead center, -0.02 = car is centered to left, 0.02 = car pointing to right
        mid = int(width / 2 * (1 + camOffset))
        xOffset = (leftX2 + rightX2) / 2 - mid

    # steering angle is the angle between navigation direction to end of center line
    yOffset = int(height / 2)

    angToMidRadian = math.atan(xOffset / yOffset)       # angle to center vertical line in radians
    angToMidDeg = int(angToMidRadian * 180.0 / math.pi)   # angle to center vertical line in degrees
    steeringAngle = angToMidDeg + 90

    return steeringAngle

def stabilizeSteeringAng(currentAngle, newAngle, numLanes, maxAngDevTwoLines=10, maxAngDevOneLine=7):

    if numLanes == 2:
        maxAngleDeviation = maxAngDevTwoLines
    else:
        maxAngleDeviation = maxAngDevOneLine

    angleDeviation = newAngle - currentAngle
    if abs(angleDeviation) > maxAngleDeviation:
        stabilizedAngle = int(currentAngle + maxAngleDeviation * angleDeviation / abs(angleDeviation))
    else:
        stabilizedAngle = newAngle
    
    return stabilizedAngle

def displayHeading(frame, angle, lineColor=(0, 0, 255), lineWidth=5):
    headingImg = np.zeros_like(frame)
    height, width, _ = frame.shape

    # figure out the heading line from steering angle
    # heading line (x1,y1) is always center bottom of the screen
    # (x2, y2) requires a bit of trigonometry

    # Note: the steering angle of:
    # 0-89 degree: turn left
    # 90 degree: going straight
    # 91-180 degree: turn right
    steeringAngleRadian = angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steeringAngleRadian))
    y2 = int(height / 2)

    cv.line(headingImg, (x1, y1), (x2, y2), lineColor, lineWidth)
    headingImg = cv.addWeighted(frame, 0.8, headingImg, 1, 1)

    return headingImg



if __name__ == '__main__':
    #frame = cv.imread("../test/Image_Proc_Demo/IMG__1692_0_1.png")

    ip = ImageProcessor(True, True)

    path = "C:/usr/training/"

    currentSteeringAngle = 90

    for file in os.listdir(path):
        if cv.waitKey(1) == ord("q"):
            break

        # get original frame
        frame = cv.imread(path + file)

        # get lines (canny)
        lines = ip.extractLines(frame)

        # get line segments
        lineSegs = ip.getLineSegments(lines)
        if lineSegs is not None:
            lineImage = displayLaneLines(frame, lineSegs)
            cv.imshow("Line Segments", lineImage)

        # combine line segments into one or two lane lines
        lanes = avgSlopeIntercept(frame, lineSegs)
        # no lanes detected
        if len(lanes) == 0:
            continue
        laneImage = displayLaneLines(frame, lanes)
        cv.imshow("Lane Lines", laneImage)

        # calculate and display steering angle
        newSteeringAngle = calcSteeringAng(frame, lanes)
        currentSteeringAngle = stabilizeSteeringAng(currentSteeringAngle, newSteeringAngle, len(lanes))
        headingImg = displayHeading(frame, currentSteeringAngle)
        cv.imshow("Heading", headingImg)

        time.sleep(0.25)
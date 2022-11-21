from ImageProcessor import *
if __name__ == '__main__':
    #frame = cv.imread("../test/Image_Proc_Demo/IMG__1692_0_1.png")

    ip = ImageProcessor(False, False)

    path = "/home/senior-design/Documents/data/9-21 Dylan-2/"
    path_save = "/home/senior-design/Documents/data2/"
    currentSteeringAngle = 90
    
    index = 1

    for file in os.listdir(path):
        if cv.waitKey(1) == ord("q"):
            break

        # get original frame
        frame = cv.imread(path + file)

        # get lines (canny)
        lines = ip.extractLines(frame)

        # get line segments
        lineSegs = ip.getLineSegments(lines)

        # combine line segments into one or two lane lines
        lanes = avgSlopeIntercept(frame, lineSegs)

        # calculate and display steering angle
        newSteeringAngle = calcSteeringAng(frame, lanes)
        currentSteeringAngle = stabilizeSteeringAng(currentSteeringAngle, newSteeringAngle, len(lanes))
        filename = "IMG__"+str(index)+"_"+str(currentSteeringAngle)+".png" 
        save_this = path_save + filename
        img = cv.imwrite(save_this,frame)
        index = index + 1 
        
        
    path = '/home/senior-design/Documents/data/9-21 Dylan-3/'


    for file in os.listdir(path):
        if cv.waitKey(1) == ord("q"):
            break

        # get original frame
        frame = cv.imread(path + file)

        # get lines (canny)
        lines = ip.extractLines(frame)

        # get line segments
        lineSegs = ip.getLineSegments(lines)

        # combine line segments into one or two lane lines
        lanes = avgSlopeIntercept(frame, lineSegs)

        # calculate and display steering angle
        newSteeringAngle = calcSteeringAng(frame, lanes)
        currentSteeringAngle = stabilizeSteeringAng(currentSteeringAngle, newSteeringAngle, len(lanes))
        filename = "IMG__"+str(index)+"_"+str(currentSteeringAngle)+".png" 
        save_this = path_save + filename
        img = cv.imwrite(save_this,frame)
        index = index + 1 
        
    path = '/home/senior-design/Documents/data/9-21 Dylan-1/'

    for file in os.listdir(path):
        if cv.waitKey(1) == ord("q"):
            break

        # get original frame
        frame = cv.imread(path + file)

        # get lines (canny)
        lines = ip.extractLines(frame)

        # get line segments
        lineSegs = ip.getLineSegments(lines)

        # combine line segments into one or two lane lines
        lanes = avgSlopeIntercept(frame, lineSegs)

        # calculate and display steering angle
        newSteeringAngle = calcSteeringAng(frame, lanes)
        currentSteeringAngle = stabilizeSteeringAng(currentSteeringAngle, newSteeringAngle, len(lanes))
        filename = "IMG__"+str(index)+"_"+str(currentSteeringAngle)+".png" 
        save_this = path_save + filename
        img = cv.imwrite(save_this,frame)
        index = index + 1 



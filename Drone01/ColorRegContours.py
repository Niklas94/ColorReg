import cv2
import numpy as np

cam = cv2.VideoCapture('tcp://192.168.1.1:5555')

#HSV Lower and Upperbounds
lowerBound1 = np.array([5,205,125], dtype=np.uint8) 
upperBound1 = np.array([8,255,255], dtype=np.uint8)
lowerBound2 = np.array([171,205,125]) 
upperBound2 = np.array([174,255,255]) 
lowerBound3 = np.array([0,125,55], dtype=np.uint8)
upperBound3 = np.array([5,255,255], dtype=np.uint8)
lowerBound4 = np.array([174,125,55], dtype=np.uint8)
upperBound4 = np.array([179,255,255], dtype=np.uint8)

#A boolean to keep running the program
running = True
#Another boolean used to check if the program gets any frame from the drone
#If it doesn't get a frame from the drone, set camFeed to false, to prevent crash when resizing frame. 
camFeed = True

while running:
    # get current frame of video    
    running, frame = cam.read()
    if frame is None:
        print("error loading frame")
        camFeed = False
    else:
        smallFrame = cv2.resize(frame,(0,0),fx=0.5,fy=0.5)
        camFeed = True
        
    #Used java to get rows in Image. Nr. of rows in front camera is 720
    rows = 720
    
    if camFeed:
        frameHSV= cv2.cvtColor(smallFrame,cv2.COLOR_BGR2HSV)
        frameGray = cv2.cvtColor(smallFrame, cv2.COLOR_BGR2GRAY)
        frameMask1 = cv2.inRange(frameHSV, lowerBound1, upperBound1)
        frameMask2 = cv2.inRange(frameHSV, lowerBound2, upperBound2)
        frameMask3 = cv2.inRange(frameHSV, lowerBound3, upperBound3)
        frameMask4 = cv2.inRange(frameHSV, lowerBound4, upperBound4)
        frameMaskfull = frameMask1 + frameMask2 + frameMask3 + frameMask4

        kernelOpen = np.ones((5,5))
        kernelClose = np.ones((20,20))
        
        frameMaskOpen = cv2.morphologyEx(frameMaskfull, cv2.MORPH_OPEN, kernelOpen)
        frameMaskClose = cv2.morphologyEx(frameMaskOpen, cv2.MORPH_CLOSE, kernelClose)

        bilateral_filtered_image = cv2.bilateralFilter(smallFrame, 5, 175, 175)
        cv2.imshow('Bilateral', bilateral_filtered_image)
        
        edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
        cv2.imshow('Edge', edge_detected_image)
         
        _, contours, _=cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        
        contour_list = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
            area = cv2.contourArea(contour)
            if ((len(approx) > 8) & (len(approx) < 23) & (area > 30)):
                contour_list.append(contour)
        cv2.drawContours(smallFrame, contour_list, -1, (0, 0, 255), 2)
        cv2.imshow('Objects Detected', smallFrame)
        cv2.imshow("HSVDrone", frameMaskfull)
        if cv2.waitKey(1) & 0xFF == 27:
            # escape key pressed
            running = False
    else:
        # error reading frame
        print('error reading video feed')
cam.release()
cv2.destroyAllWindows()
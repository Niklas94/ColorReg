import cv2
import numpy as np

#Remember to connect to AR-drone wifi
cam = cv2.VideoCapture('tcp://192.168.1.1:5555')

#HSV lower and upperbounds
lowerBound1 = np.array([5,205,125], dtype=np.uint8) 
upperBound1 = np.array([8,255,255], dtype=np.uint8)
lowerBound2 = np.array([171,205,125], dtype=np.uint8) 
upperBound2 = np.array([174,255,255], dtype=np.uint8) 

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
    #rows = 720
    if camFeed:
        frameHSV= cv2.cvtColor(smallFrame,cv2.COLOR_BGR2HSV)
        frameMask1 = cv2.inRange(frameHSV, lowerBound1, upperBound1)
        frameMask2 = cv2.inRange(frameHSV, lowerBound2, upperBound2)
        frameMask3 = cv2.inRange(frameHSV, lowerBound3, upperBound3)
        frameMask4 = cv2.inRange(frameHSV, lowerBound4, upperBound4)
        frameMaskfull = frameMask1 + frameMask2 + frameMask3 + frameMask4
        
        kernelOpen = np.ones((5,5))
        kernelClose = np.ones((20,20))
        
        frameMaskOpen = cv2.morphologyEx(frameMaskfull, cv2.MORPH_OPEN, kernelOpen)
        frameMaskClose = cv2.morphologyEx(frameMaskOpen, cv2.MORPH_CLOSE, kernelClose)
        
        frameMaskBoth = frameMaskOpen + frameMaskClose
        
        cv2.imshow("Raw", smallFrame)
        cv2.imshow("HSV", frameHSV)
        #cv2.imshow("Mask Open", frameMaskOpen)
        #cv2.imshow("Mask Closed", frameMaskClose)
        cv2.imshow("Masks applied", frameMaskfull) 
        
        if cv2.waitKey(1) & 0xFF == 27:
            # escape key pressed
            running = False

    else:
        # error reading frame
        print('error reading video feed')
cam.release()
cv2.destroyAllWindows()
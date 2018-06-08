import cv2
import numpy as np

cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
#cam = cv2.VideoCapture(0)
#lowerBound1 = np.array([33,80,40])
#upperBound1 = np.array([102,255,255])

#Link til findContours: https://stackoverflow.com/questions/32287032/circular-hough-transform-misses-circles

#HSV (H: 0-179, S: 0-255, V: 0-255)

#Hue is the degree of color range from 0-360 (downscaled in opencv from 0-179) example: red is 170-179 + 0-10 (overlaps, thats why we have 2x lower and upperbounds)
#Saturation is how strong the color is, example 255 is 100% red (if hue is the red color) and a saturation of 0 will always make the camera detect white colors, no matter the hue.
#Value is the spectrum of the color, how dark/light it is, example dark red and light red.

#More variation

lowerBound1 = np.array([5,205,125], dtype=np.uint8) 
upperBound1 = np.array([8,255,255], dtype=np.uint8)
lowerBound2 = np.array([171,205,125]) 
upperBound2 = np.array([174,255,255]) 

#Dark and light red:

lowerBound3 = np.array([0,125,55], dtype=np.uint8)
upperBound3 = np.array([5,255,255], dtype=np.uint8)
lowerBound4 = np.array([174,125,55], dtype=np.uint8)
upperBound4 = np.array([179,255,255], dtype=np.uint8)

#Retarded ring
#127, 92, 58
lowerBound5 = np.array([126,85,52], dtype=np.uint8)
upperBound5 = np.array([128,100,65], dtype=np.uint8)

counter = 0;
running = True
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
    #counter = counter + 1
   
    #Used java to get rows in Image. Nr. of rows in front camera is 720
    rows = 720
    
    
    if camFeed:
        frameHSV= cv2.cvtColor(smallFrame,cv2.COLOR_BGR2HSV)
        frameGray = cv2.cvtColor(smallFrame, cv2.COLOR_BGR2GRAY)
        frameMask1 = cv2.inRange(frameHSV, lowerBound1, upperBound1)
        frameMask2 = cv2.inRange(frameHSV, lowerBound2, upperBound2)
        frameMask3 = cv2.inRange(frameHSV, lowerBound3, upperBound3)
        frameMask4 = cv2.inRange(frameHSV, lowerBound4, upperBound4)
        frameMaskRR = cv2.inRange(frameHSV, lowerBound5, upperBound5)
        frameMaskfull = frameMask1 + frameMask2 + frameMask3 + frameMask4 + frameMaskRR
        
        
        
        #red = np.uint8([[[43, 47, 179]]])
        #hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
        #print(hsv_red)
        
        #red = np.uint8([[[58, 37, 42]]])
        #hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
        #print(hsv_red)
        
        kernelOpen = np.ones((5,5))
        kernelClose = np.ones((20,20))
        
        frameMaskOpen = cv2.morphologyEx(frameMaskfull, cv2.MORPH_OPEN, kernelOpen)
        frameMaskClose = cv2.morphologyEx(frameMaskOpen, cv2.MORPH_CLOSE, kernelClose)
        
        #Awesome edge start
        
        #Default is smallFrame
        bilateral_filtered_image = cv2.bilateralFilter(smallFrame, 5, 175, 175)
        cv2.imshow('Bilateral', bilateral_filtered_image)
        
        #default value: bilateral_filtered_image
        edge_detected_image = cv2.Canny(frameMaskfull, 75, 200)
        cv2.imshow('Edge', edge_detected_image)
         
        #Default value var edge_detected_image i stedet for frameMaskfull
        _, contours, _=cv2.findContours(frameMaskfull, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        
        contour_list = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
            area = cv2.contourArea(contour)
            if ((len(approx) > 8) & (len(approx) < 23) & (area > 30)):
                contour_list.append(contour)
        cv2.drawContours(smallFrame, contour_list, -1, (0, 0, 255), 2)
        cv2.imshow('Objects Detected', smallFrame)
        
        #blur = cv2.GaussianBlur(frame,(5,5),0)
        #edge_detected_image = cv2.Canny(blur, 75, 200)
        #cv2.imshow("blur", blur)
        #cv2.imshow("Edge", edge_detected_image)  
        #_, contours, _= cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        ##_, contours, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #contour_list = []
        #for contour in contours:
        #    approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
        #    area = cv2.contourArea(contour)
            #Default values: 8, 23 and 30
            #if ((len(approx) > 8) & (len(approx) < 23) & (area > 30)):
        #    if ((len(approx) > 15)):
        #        contour_list.append(contour)
        #default values: img, contour_listm -1, (0,0,255), 2)        
        #cv2.drawContours(blur, contour_list, -1, (0,0,255), 2)
        #cv2.imshow("Circles Detected", frameMaskfull)
          
        #Awesome edge stop  
          
        #cv2.imshow("Mask open", frameMaskOpen)
        #cv2.imshow("Mask close", frameMaskClose)
        cv2.imshow("HSVDrone", frameMaskfull)
        #cv2.imshow("Drone", frame)
        #cv2.imshow("gray",frameGray)
        if cv2.waitKey(1) & 0xFF == 27:
            # escape key pressed
            running = False
       # if counter.__eq__(1):
        #circles = cv2.HoughCircles(frameGray, cv2.HOUGH_GRADIENT, 1, rows, param1=100, param2=30, minRadius=100, maxRadius=500)
       # circles =  cv2.findContours(frameMaskfull, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #if circles is None:
        #    print("dude")
        #else:
            #circles = np.uint16(np.round(circles))
            #print circles
            #np.around(circles)
            #for i in circles[0,:]:
                #Draw green circle around detected rings
            #    cv2.circle(frameGray,(i[0],i[1]),i[2],(0,255,0),2)
                #Draw dot in center of rings
            #    cv2.circle(frameGray,(i[0],i[1]),2,(0,0,255),3)
            #    counter=0
        #    cv2.drawContours(frameMaskfull, circles, -1, color=(0,0,255), thickness=1) 
        #    cv2.imshow("Detected circles", frameMaskfull) 
    else:
        # error reading frame
        print('error reading video feed')
cam.release()
cv2.destroyAllWindows()
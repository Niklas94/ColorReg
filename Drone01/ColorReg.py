import cv2
import numpy as np

cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
#cam = cv2.VideoCapture(0)
#lowerBound1 = np.array([33,80,40])
#upperBound1 = np.array([102,255,255])

#HSV (H: 0-179, S: 0-255, V: 0-255)

lowerBound1 = np.array([0,70,50], dtype=np.uint8)
upperBound1 = np.array([10,255,255], dtype=np.uint8)
lowerBound2 = np.array([170,70,50]) #ubetydlig atm.
upperBound2 = np.array([180,255,255]) #ubetydlig atm.
running = True

while running:
    # get current frame of video    
    running, frame = cam.read()
    if running:
        frameHSV= cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
        frameMask1 = cv2.inRange(frameHSV, lowerBound1, upperBound1)
        frameMask2 = cv2.inRange(frameHSV, lowerBound2, upperBound2)
        frameMaskfull = frameMask1 + frameMask2
        
       # red = np.uint8([[[43, 47, 179]]])
       # hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
       # print(hsv_red)
        
        kernelOpen = np.ones((5,5))
        kernelClose = np.ones((20,20))
        
        frameMaskOpen = cv2.morphologyEx(frameMaskfull, cv2.MORPH_OPEN, kernelOpen)
        framMaskClose = cv2.morphologyEx(frameMaskOpen, cv2.MORPH_CLOSE, kernelClose)
          
        cv2.imshow("Mask open", frameMaskOpen)
        cv2.imshow("Mask close", framMaskClose)
        cv2.imshow("HSVDrone", frameMaskfull)
        cv2.imshow("Drone", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            # escape key pressed
            running = False
    else:
        # error reading frame
        print('error reading video feed')
cam.release()
cv2.destroyAllWindows()
import cv2
import numpy as np

def nothing(x):
    pass
cap = cv2.VideoCapture(0)
cv2.namedWindow('image',cv2.CV_WINDOW_AUTOSIZE)

# create trackbars for color change
cv2.createTrackbar('Hlow','image',0,179,nothing)
cv2.createTrackbar('Slow','image',0,255,nothing)
cv2.createTrackbar('Vlow','image',0,255,nothing)

cv2.createTrackbar('Hhigh','image',0,179,nothing)
cv2.createTrackbar('Shigh','image',0,255,nothing)
cv2.createTrackbar('Vhigh','image',0,255,nothing)
frame = cv2.imread('rectified.pgm')
while(1):
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    hlow = cv2.getTrackbarPos('Hlow','image')
    slow = cv2.getTrackbarPos('Slow','image')
    vlow = cv2.getTrackbarPos('Vlow','image')

    hhigh = cv2.getTrackbarPos('Hhigh','image')
    shigh = cv2.getTrackbarPos('Shigh','image')
    vhigh = cv2.getTrackbarPos('Vhigh','image')

    lb = np.array([hlow,slow,vlow])
    ub = np.array([hhigh,shigh,vhigh])

    hsvimg = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsvimg,lb,ub)
    res = cv2.bitwise_and(frame,frame,mask=mask)
    cv2.imshow('frame',res)

cap.release()
cv2.destroyAllWindows()

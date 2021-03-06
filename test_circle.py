import cv2
import numpy as np
import sys

def circle_nocolor():
    src = cv2.imread(str(sys.argv[1]),cv2.IMREAD_COLOR)
    output = src.copy()
    gray = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    gray  = cv2.GaussianBlur(gray, (5,5), 0)   
    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 2, 2)
    cv2.imwrite("GRAY.Png",gray)
    if circles is not None:
        print len(circles)
        circles = np.round(circles[0,:]).astype("int")
        for (x,y,r) in circles:
            cv2.circle(output, (x,y), r, (0,255,0),4)
            cv2.rectangle(output,(x-5,y-5),(x+5,y+5),(0,128,255),-1)
            cv2.imshow("output", np.hstack([src,output]))
            cv2.waitKey(0)
    


if __name__ == '__main__':
    circle_nocolor()

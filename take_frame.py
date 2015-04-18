#!/usr/bin/env python
import cv2


def take_frame():
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    s, img = cam.read()
    if s:   
        cv2.imwrite("rectified.jpg",img) #save image

if __name__ == '__main__':
    take_frame()

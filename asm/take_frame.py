#!/usr/bin/env python
import cv2


def take_frame():
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    s, img = cam.read()
    return img

if __name__ == '__main__':
    take_frame()

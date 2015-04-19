'''
Main detection python code for team software. 
Used with a usb webcam

Written by team software (Zack Smith & Taylor Million) 1/25/15

Todo:

-Rosify Heartbeat code
-Crop Images
-Adjust and optimize navigation
-Take image every x seconds 

''' 

# Imports 
from subprocess import call
from sys import argv,exit
from threading import Timer
from team_software.msg import RandTheta

# Real modules
import cv2
import colordetection as cd
import time
import rospy

# My shitty modules
import take_frame as fcap

def detection_loop():
        # Grab frame
        frame = fcap.take_frame()
	(r,angle_out) = cd.color_detect(frame)
	return (r,angle_out)

def main():
        payload.theta = detection_loop()  
  
# Boiler plate code
if __name__ == '__main__':
    try: 
	main()
    except rospy.ROSInterruptException:
	pass


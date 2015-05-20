#!/usr/bin/env python
'''
Code to take and save frames and disparities using the bumblebee2 camera
Writes data based off of curent time
-Timestamp:  YYYYMMDDHHMMSS in UTC
Probably wildly inefficient

Written by Zack Smith (5-19-15)
''' 

# Imports 
from subprocess import call

# Real modules
import cv2
from time import strftime, gmtime
import rospy


def get_data():
	''' 
	Function to obtain & save two main data points:
	-Rectified image
	-Disparity for said image
	'''
        # Grab frame
	cpp_file = "./triclops/src/examples/common/stereoto3dpoints/stereoto3dpoints"
	call(cpp_file)
	

def main():
        get_data()

# Boiler plate code
if __name__ == '__main__':
    try: 
	main()
    except rospy.ROSInterruptException:
	pass


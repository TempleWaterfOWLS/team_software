#!/usr/bin/env python
'''
Code to take and save frames and disparities using the bumblebee2 camera
Writes data based off of curent time
-Timestamp:  YYYYMMDDHHMMSS in UTC
Probably wildly inefficient

Written by Zack Smith (5-19-15)
''' 

# Imports 
# Call required for triclops code
from subprocess import call
# Import for filename writing
from time import strftime, gmtime
# OS imports for file sorting and bash scripting
from os import system

def get_data():
	''' 
	Function to obtain & save two main data points:
	-Rectified image
	-Disparity for said image
	'''
        # Grab frame
	cpp_file = "../triclops/src/examples/common/stereoto3dpoints/stereoto3dpoints"
	call(cpp_file)
	# Files created are out.pts and rectified.pgm
	timestamp = strftime("%Y%m%d%H%M%S",gmtime())
	# Save files to temp storage
	try:
		system("cp rectified.pgm ./frames/" + timestamp + ".pgm")
		system("cp out.pts ./disparity/" + timestamp + ".pts")
	except:
		pass

def main():
        get_data()

# Boiler plate code
if __name__ == '__main__':
    try: 
	main()
    except rospy.ROSInterruptException:
	pass


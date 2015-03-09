'''
Main python code for team software. Calls all other functions required for operation. 
Ideally, it will contain: 
-An Algorithmic State Machine (ASM) to determine current task
-Function calls to appropriate tasks
-Ability to pass data from sensors to different modules

Written by team software (Zack Smith & Taylor Million) 1/25/15

Todo: Everything
Usage: Not yet determined
''' 

# Imports 
from subprocess import call
from sys import argv,exit
from threading import Timer
from team_software.msg import RandTheta

import cv2
import colordetection as cd
import time
import rospy


def detection_loop(args):
	for ctr,arg in enumerate(args):
		print ctr,arg
	cpp_file = args[0]; reconstruct_file = args[1]; rectified_file = args[2];
	print cpp_file
	call(cpp_file)
   	call([reconstruct_file])
	angle_out = cd.color_detect(['rectified.pgm'])
	return angle_out

def main():
    # Ros publisher stuff
    pub = rospy.Publisher('RandTheta', RandTheta, queue_size=1)
    rospy.init_node('nav_node')
    payload = RandTheta(); payload.theta = 0; payload.r = 0
    rate = rospy.Rate(10)
    # Not ROS publisher stuff
    stdin_args = ''
    cpp_file = "./triclops/src/examples/common/stereoto3dpoints/stereoto3dpoints"
    reconstruct_file = "./triclops/src/examples/common/stereoto3dpoints/reconstruction.py"
    rectified_file = 'rectified.pgm'
    # Parse for inputs
    if len(argv) == 2:
	cpp_file = argv[1]
    elif len(argv) == 3:
	cpp_file = argv[1]
	stdin_args = argv[2]
	# Try to call C++ file
	cpp_file = "./" + cpp_file
	cpp_file = [cpp_file]
    while not rospy.is_shutdown():
	try:
	    args = [cpp_file,reconstruct_file,rectified_file,stdin_args]
	    payload.theta = detection_loop(args)  
	except:
	    print 'Except block, default'
	    payload.theta = 90.0
	# Publish this shit yo
	pub.publish(payload)
	rate.sleep()
	
# Boiler plate code
if __name__ == '__main__':
    try: 
	main()
    except rospy.ROSInterruptException:
	pass


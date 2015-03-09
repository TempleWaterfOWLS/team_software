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
import cv2
import colordetection as cd
import time

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
	while 1:
		try:
			args = [cpp_file,reconstruct_file,rectified_file,stdin_args]
			angle_out = detection_loop(args)  
		except:
			print 'Except block, default'
			angle_out = 90
		# After navigation, call motor code
		# motor_code(angle_out)
		print 'before sleep'
		time.sleep(10)
		print 'after sleep'
		# Call motor code to drive forward
		# motor_code(0)
		# Rerun detection loop
	
# Boiler plate code
if __name__ == '__main__':
    main()



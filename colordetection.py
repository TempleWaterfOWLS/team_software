"""
USAGE: python colordetection.py ~/file/path/to/jpg/file.jpg

This function should recieve an input picture filepath, and then return whether or not a specific color was detected in a significant fashion. Colors to be detected for every task: 

Red, White, Green			Starting Gates
Yellow, Black 				Obstacles
Yellow, Black, Blue, Green, Red		Acoustic Pinger Buoys
Yellow, Blue, Green, Red, White		Underwater Light Detection

**************This function has not been properly tested********************

TODO: 
1)Get better HSV values for all the colors

2)Attempt to threshold better (Erosion? Small particle filter?)

3)Return whether or not a color was detected - perhaps hand in hand with shape detection (only return if shape is a circular buoy).

4)Incorporate ambient light data for dynamic color thresholding?

"""

import sys 		
import cv	
import cv2
import numpy as np

def color_detect(argv):
	'''
	# Debug Info
	print 'Number of arguments:', len(argv), 'arguments.'
	print 'Argument List:', str(argv)
	# Grab picture filepath, convert to string:
	'''
	filepath = str(argv[0])
	#print filepath
	# Define HSV bounds for Black, Blue, Green, Red, White, Yellow, Random obstacles:
	lower_black  = np.array([0,0,20]);    upper_black  = np.array([180,35,53])
	lower_blue   = np.array([100,45,40]); upper_blue   = np.array([161,114,130])
	lower_green  = np.array([26,50,50]);  upper_green  = np.array([180,255,255])
	lower_red    = np.array([174,50,50]); upper_red    = np.array([180,255,255])        
	lower_yellow = np.array([18,50,133]); upper_yellow = np.array([28,120,255])

        #Less strict BBall: [0 97 51], [179 152 149]
	#lower_bball = np.array([0,84,51]); upper_bball = np.array([179,128,87])
	lower_bball = np.array([2,111,0]); upper_bball = np.array([7,179,219])
        #Strict Soccer Ball: [0 0 24] [179 100 41]
	lower_sball = np.array([0,0,24]); upper_sball = np.array([179,100,41])        

        # White not really defined so well
	lower_white  = np.array([0,0,255])
	upper_white  = np.array([10,0,255])

	#Read image in and convert to HSV
	img = cv2.imread(filepath,cv2.IMREAD_COLOR)
	hsvimg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	#Apply Thresholding for different colors:
	black_mask  = cv2.inRange(hsvimg,lower_black,upper_black)
	blue_mask   = cv2.inRange(hsvimg,lower_blue,upper_blue)
	green_mask  = cv2.inRange(hsvimg,lower_green,upper_green)
	red_mask    = cv2.inRange(hsvimg,lower_red,upper_red)
	white_mask  = cv2.inRange(hsvimg,lower_white,upper_white)
	yellow_mask = cv2.inRange(hsvimg,lower_yellow,upper_yellow)	
	bball_mask  = cv2.inRange(hsvimg,lower_bball,upper_bball)	
	sball_mask  = cv2.inRange(hsvimg,lower_sball,upper_sball)	        

	#Apply different morphological filters to get appropriate shape and remove noise (Needs testing):
	close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))	
	open_kernel  = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))	
	#closing = cv2.morphologyEx(bluemask,cv2.MORPH_CLOSE,closekernel)
	sball_opening = cv2.morphologyEx(sball_mask,cv2.MORPH_OPEN,open_kernel)	
	bball_opening = cv2.morphologyEx(bball_mask,cv2.MORPH_OPEN,open_kernel)	

	res = cv2.bitwise_and(img,img,mask = bball_mask)
	res2 = cv2.bitwise_and(img,img,mask = sball_mask)
	res3 = cv2.bitwise_and(img,img,mask = sball_opening)
        res4 = cv2.bitwise_and(img,img,mask = bball_opening) 

	#Display Pictures
	cv2.namedWindow('img', cv2.WINDOW_NORMAL)
	cv2.imshow('img',img)
	cv2.namedWindow('bballmask', cv2.WINDOW_NORMAL)
	cv2.imshow('bballmask',res)
	cv2.namedWindow('bballopen', cv2.WINDOW_NORMAL)
	cv2.imshow('bballopen',res4)
	cv2.namedWindow('sballmask',cv2.WINDOW_NORMAL)
	cv2.imshow('sballmask',res2)
	cv2.namedWindow('sballopen',cv2.WINDOW_NORMAL)
	cv2.imshow('sballopen',res3)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def main(argv):
	# Call color detect
	color_detect(argv)

if __name__ == "__main__":
	# Pass in system inputs
	main(sys.argv[1:])



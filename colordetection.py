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

4)Get pixel size? Make new function for calculating pixel size / centroid / etc ?

5)Return whether or not a color was detected - perhaps hand in hand with shape detection (only return if shape is a circular buoy).

6) Incorporate ambient light data for dynamic color thresholding?

"""
import sys 		
import cv	
import cv2
import numpy as np

def color_detect(argv):
	print 'Number of arguments:', len(argv), 'arguments.'
	print 'Argument List:', str(argv)

	# Define HSV bounds for Black, Blue, Green, Red, White Yellow:
	# None of these values have been tested.
	# Red, Green, Blue, and Yellow are based off of competition papers	 
	# Black and White are off of RGB data. 	
	lower_black  = np.array([0,0,0])
	upper_black  = np.array([10,0,0])

	lower_blue   = np.array([100,125,0])
	upper_blue   = np.array([115,255,255])
	
	lower_green  = np.array([50,50,0])
	upper_green  = np.array([80,255,255])

	lower_red    = np.array([0,110,0])
	upper_red    = np.array([10,255,255])

	lower_white  = np.array([0,0,255])
	upper_white  = np.array([10,0,255])

	lower_yellow = np.array([25,160,160])
	upper_yellow = np.array([40,255,255])

	# Grab picture filepath, convert to string:
	filepath = str(argv[0])
	print filepath
	
	#Read image in:
	img = cv2.imread(filepath,cv2.IMREAD_COLOR)

	#Convert Image to HSV Space:
	hsvimg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	#Apply Thresholding for different colors:
	black_mask  = cv2.inRange(hsvimg,lower_black,upper_black)
	blue_mask   = cv2.inRange(hsvimg,lower_blue,upper_blue)
	green_mask  = cv2.inRange(hsvimg,lower_green,upper_green)
	red_mask    = cv2.inRange(hsvimg,lower_red,upper_red)
	white_mask  = cv2.inRange(hsvimg,lower_white,upper_white)
	yellow_mask = cv2.inRange(hsvimg,lower_yellow,upper_yellow)	

	#Apply different morphological filters to get appropriate shape and remove noise (Needs testing):

	close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))	
	open_kernel  = cv2.getStructuringElement(cv2.MORPH_RECT,(10,10))
	
	#closing = cv2.morphologyEx(bluemask,cv2.MORPH_CLOSE,closekernel)
	opening = cv2.morphologyEx(blue_mask,cv2.MORPH_OPEN,open_kernel)	

	res = cv2.bitwise_and(img,img,mask = yelow_mask)
	res2 = cv2.bitwise_and(img,img,mask = opening)

	#Display Pictures
	cv2.namedWindow('img', cv2.WINDOW_NORMAL)
	cv2.imshow('img',img)
#	cv2.namedWindow('hsvimg', cv2.WINDOW_NORMAL)
#	cv2.imshow('hsvimg',hsvimg)
	cv2.namedWindow('bluemask', cv2.WINDOW_NORMAL)
	cv2.imshow('bluemask',blue_mask)
	cv2.namedWindow('Opening', cv2.WINDOW_NORMAL)
	cv2.imshow('Opening',opening)
	cv2.namedWindow('result',cv2.WINDOW_NORMAL)
	cv2.imshow('result',res)
	cv2.namedWindow('res2',cv2.WINDOW_NORMAL)
	cv2.imshow('res2',res2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return blue_mask,opening

def main(argv):
	res1,res2 = color_detect(argv)
	cv2.namedWindow('test', cv2.WINDOW_NORMAL)
	cv2.imshow('test',res1)
	cv2.namedWindow('test2', cv2.WINDOW_NORMAL)
	cv2.imshow('test2',res2)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main(sys.argv[1:])



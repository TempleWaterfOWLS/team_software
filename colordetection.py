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
	centerline = img.shape[1] / 2

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
	open_kernel  = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))	
	#closing = cv2.morphologyEx(bluemask,cv2.MORPH_CLOSE,closekernel)
	sball_opening = cv2.morphologyEx(sball_mask,cv2.MORPH_OPEN,open_kernel)	
	bball_opening = cv2.morphologyEx(bball_mask,cv2.MORPH_OPEN,open_kernel)	

	res = cv2.bitwise_and(img,img,mask = bball_mask)
	res2 = cv2.bitwise_and(img,img,mask = sball_mask)
	res3 = cv2.bitwise_and(img,img,mask = sball_opening)
   	res4 = cv2.bitwise_and(img,img,mask = bball_opening)

	# Find contours of specific masks
	bball_cont = bball_mask.copy()
	thresh_src = np.zeros((bball_cont.shape[0], bball_cont.shape[1],3),np.uint8)
	thresh_src[:] = (255,255,255)	
	contours,hierarchy = cv2.findContours(bball_cont, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# Hold important contour information
	ctr = 0; centroids = []
	for num in range(len(contours)):
		if len(contours[num]) > 20:
			# Get bounding rectangle coordinates
			x,y,w,h = cv2.boundingRect(contours[num])
			cv2.rectangle(thresh_src,(x,y),(x+w,y+h),(0,255,0),2)
			centroids.append([x+w/2, y+h/2]) 
			# Draw Contours
			cv2.drawContours(thresh_src,contours,num,(0,0,0),1)
			ctr += 1	
	# Write to file for debugging purposes
	cv2.imwrite("Area Thresh.png",thresh_src)
	print ctr
	left_side = 0; right_side = 0;
	# Iterate over centroids, seeing where they lie with respect to the center line
	for centroid in centroids:
		# Check x position for left/right of centerline
		if centroid[0] > centerline:
			right_side += 1
		else:
			left_side += 1			
	print 'RIGHT ' + str(right_side)
	print 'LEFT ' + str(left_side)
	
	# Lazy output logic: 
	# If right > left, go left (return negative)
	# Else go right (return positive)
	if right_side > left_side:
		print "90"
		return 90
	elif right_side == 0 and left_side == 0:
		print "0"
		return 0
	else:
		print "-90"
		return -90	
	
	'''
	src = cv2.imread("yoloswag420.png")
	output = src.copy()
	gray = bball_cont
	#gray = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)

    	circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 50, 10, param1=50, param2=30, minRadius=0, maxRadius=0)
    	cv2.imwrite("GRAY.Png",gray)
    	if circles is not None:
		circles = np.round(circles[0,:]).astype("int")
	        for (x,y,r) in circles:
        	    cv2.circle(output, (x,y), r, (0,255,0),4)
        	    cv2.rectangle(output,(x-5,y-5),(x+5,y+5),(0,128,255),-1)
        	    cv2.imshow("output", np.hstack([src,output]))
        	    
    '''


	
	#Display Pictures
	cv2.namedWindow('img', cv2.WINDOW_NORMAL)
	cv2.imshow('img',img)
	cv2.namedWindow('bballmask', cv2.WINDOW_NORMAL)
	cv2.imshow('bballmask',res)
	cv2.namedWindow('bball_cont', cv2.WINDOW_NORMAL)
	cv2.imshow('bball_cont',bball_cont)
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



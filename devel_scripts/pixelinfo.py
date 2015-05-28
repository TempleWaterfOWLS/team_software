import sys 		
import cv	
import cv2
import numpy as np
import colordetection

""" 
USAGE: python pixelinfo.py ~/path/to/image

This function is dependent on the colordetection.py function, so make sure you have that in the same directory as this!

pixel_info should take 1 to several binary image inputs, and return geometry info, size info, and centroid info about a shape shown in the binary images.

TODO: Everything.
1) Take a binary image, and return size info (contour area?)
2) Take binary image, and return geometry info (is it circular?)
3) Take binary image, and return centroid info (Find center pixel of individual contour?)
4) Take binary image, and return angle to detected obstacle (I have no idea how to do this)
5) If no significant info is found, it should return to colordetection
6) Apply area thresholding to eliminate nonimportant contours example:
	-iterate through contour areas
	-pick contour with largest area as most significant
	-check geometry
	-if circle, pass info on
	-else, find next max
7) Count amount of buoys detected, and pass all information to pathfinding/distance algorithms.  

"""

def pixel_info(binary_img):
	print "hello world" 
		
	
def main(argv):
	args = colordetection.color_detect(argv)
	print len(args)	
	if (args == None):
		print "It didn't load an image!"
	pixel_info(args[0])

if __name__ == "__main__":
	main(sys.argv[1:])



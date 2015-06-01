'''
Module for obstacle avoidance
Publishes:
-completion information (SuicideTask)
-Motor speed information (RandTheta)

Attempts to navigate around obstacles... I guess

'''

# Import for grabbing functions not in folder
import sys
sys.path.insert(0,'..')
# Imports for grabbing most recent frame
from os import listdir
from os.path import getmtime, isfile, join
# Roboboat functions
import colordetection as cd
import take_frame as tf
# ROS imports
import rospy

# Publish messages
from team_software.msg import SuicideTask
from team_software.msg import RandTheta


def main():
        # ROS publisher stuff
	suicide_pub = rospy.Publisher('SuicideTask',SuicideTask, queue_size=10)
        rtheta_pub = rospy.Publisher('RandTheta',RandTheta, queue_size=10)
        rospy.init_node('obstaclenode')
        rate = rospy.Rate(10)
        # Initialize messages
        suicide_msg = SuicideTask(); suicide_msg.suicidetask = False
        rtheta_msg = RandTheta(); rtheta_msg.r = 0; rtheta_msg.theta = 0; 
	framepath = './frames'
	disparitypath = './disparity'
        # Main loop
        frame = ''
	while not rospy.is_shutdown():
                old_frame = frame
		# Grab most recent image and disparity
		ffiles = [f for f in listdir(framepath) if isfile(join(framepath,f)) ]
		dfiles = [f for f in listdir(disparitypath) if isfile(join(disparitypath,f)) ]
		frame = max(ofiles,key=getmtime)
		disparity_file = max(dfiles,key=getmtime)
                # Check to make sure processing is not done on same image twice
                if old_frame != frame:
                        # Run color detection on it
                        (rtheta_msg.r,rtheta_msg.theta) = cd.color_detect(cv2.imread(frame))
                # Publish task status
                suicide_pub.publish(suicide_msg)
                # Publish Motor stuff
                rtheta_pub.publish(rtheta_msg)
                # Sleep for important reasons
                rate.sleep()

if __name__ == '__main__':
	main()

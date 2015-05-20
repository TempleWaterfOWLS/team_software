'''
Module for obstacle avoidance
Publishes:
-completion information (SuicideTask)
-Motor speed information (RandTheta)

Attempts to navigate around obstacles... I guess

'''

import sys
sys.path.insert(0,'..')
import obstacle_avoidance_main as OA
import time
import rospy
# Import time stuff like a champ for filename writing
from time import strftime, sleep, gmtime
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
        # Main loop
	while not rospy.is_shutdown():
		# Grab most recent image and disparity
                (rtheta_msg.r,rtheta_msg.theta) = OA.detection_loop()
                # Publish task status
                suicide_pub.publish(suicide_msg)
                # Publish Motor stuff
                rtheta_pub.publish(rtheta_msg)
                # Sleep for important reasons
                rate.sleep()

if __name__ == '__main__':
	main()

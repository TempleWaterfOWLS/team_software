'''
Module for the first task, speed gates
Publishes:
-completion information (SuicideTask)
-Motor speed information (RandTheta)

Attempts to navigate between two buoys, which are red and green

'''
import time
import rospy
# Publish messages
from team_software.msg import SuicideTask
from team_software.msg import RandTheta

def main():
        # ROS publisher stuff
 	counter = 0
	suicide_pub = rospy.Publisher('SuicideTask',SuicideTask, queue_size=10)
        rtheta_pub = rospy.Publisher('RandTheta',RandTheta, queue_size=10)
        rospy.init_node('speednode')
        rate = rospy.Rate(10)
        # Initialize messages
        suicide_msg = SuicideTask(); suicide_msg.suicidetask = False
        rtheta_msg = RandTheta(); rtheta_msg.r = 0; rtheta_msg.theta = 0; 
        # Main loop
	while not rospy.is_shutdown():
                # Do main code
                # Just go straight
                rtheta_msg.r = 2;
                # Publish task status
                suicide_pub.publish(suicide_msg)
                # Publish Motor stuff
                rtheta_pub.publish(rtheta_msg)
                # Sleep for important reasons
                rate.sleep()
		counter += 1
		print 'swag'
		if (counter == 5): suicide_msg.suicidetask = True
if __name__ == '__main__':
	main()

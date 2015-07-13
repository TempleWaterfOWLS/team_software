'''
Module for the first task, speed gates
Publishes:
-completion information (SuicideTask)
-Motor speed information (RandTheta)

Attempts to navigate between two buoys, which are red and green
'''

# Libraries used for sending requests to server
import time
import requests
import sys

# ROS stuff
import rospy
# Publish messages
from team_software.msg import SuicideTask
from team_software.msg import RandTheta
from beagleboneblack.msg import MotorPower

def start_request(IP,active_course):
	'''
	Function to signal the start of the run via HTTP
	'''
	# Construct URL
	schema = 'http://'; port='3333';teamCode='TUCE'
	start_path = '/run/start/' + active_course + '/' + teamCode
	start_url = schema + IP  + ':' + port +  start_path
	# Debugging info
	print 'Sending request to: '
	print start_url
	# Send POST request
	post_response = requests.post(start_url)
	# Send request one more time only in case of error
	if 'ERROR' in post_response.text:
		time.sleep(2)
		post_response = requests.post(start_url)


def main():
	# Get arguments passed by task checker
	IP = sys.argv[1]; active_course = sys.argv[2]
	# ROS publisher stuff
 	counter = 0
	suicide_pub = rospy.Publisher('SuicideTask',SuicideTask, queue_size=10)
        rtheta_pub = rospy.Publisher('RandTheta',RandTheta, queue_size=10)
	power_pub = rospy.Publisher('motor_power',MotorPower,queue_size=10)
        rospy.init_node('speednode')
        rate = rospy.Rate(10)
        # Initialize messages
        suicide_msg = SuicideTask(); suicide_msg.suicidetask = False
        rtheta_msg = RandTheta(); rtheta_msg.r = 2; rtheta_msg.theta = 90; 
	power_msg = MotorPower(); power_msg.power2 = 0.30; power_msg.power1 = 0.13;
	# Go straight until some condition not yet defined is met
	power_pub.publish(power_msg)
	# Send request for start challenge
	try:
		start_request(IP,active_course)
	except:
		print 'Networking error occured!'
		pass
        # Main loop
	start_time = time.time()
	while not rospy.is_shutdown():
		new_time = time.time()
		print 'Time elapsed is:',
		print new_time - start_time
                # Just go straight
		power_pub.publish(power_msg)
                # Publish task status
                #suicide_pub.publish(suicide_msg)
                # Sleep for important reasons
                rate.sleep()

if __name__ == '__main__':
	main()

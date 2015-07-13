'''
Module for the first task, speed gates
Publishes:
-completion information (SuicideTask)
-Motor speed information (RandTheta)

Attempts to navigate between two buoys, which are red and green

'''
import time
import rospy
import requests
# Publish messages
from team_software.msg import SuicideTask
from team_software.msg import RandTheta
from beagleboneblack.msg import MotorPower

def start_request():
	# Ping shore computer
	schema = 'http://'; authority = '192.168.0.106';port='3333';teamCode='TUCE'
	course = ['courseA','courseB','openTest']
	active_course = course[1]
	start_path = '/run/start/' + active_course + '/' + teamCode
	start_url = schema + authority + ':' + port +  start_path
	print 'sending request to '
	print start_url
	post_response = requests.post(start_url)
	if 'ERROR' in post_response.text:
		time.sleep(2)
	post_response = requests.post(start_url)


def main():
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
	#rtheta_pub.publish(rtheta_msg)
	power_pub.publish(power_msg)
	# Send request for start challenge
	try:
		start_request()
	except:
		print 'EXCEPTION'
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

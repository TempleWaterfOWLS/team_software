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

def gate_request():
	# Ping shore computer
	schema = 'http://'; authority = '192.168.0.106';port='3333';teamCode='TUCE'
	course = ['courseA','courseB','openTest']
	active_course = course[1]
	obs_path = '/obstacleAvoidance/' + active_course + '/' + teamCode
	obs_url = schema + authority + ':' + port +  obs_path
	print 'sending request to '
	print obs_url
	get_response = requests.get(obs_url)
	if 'ERROR' in post_response.text:
		time.sleep(2)
	get_response = requests.post(start_url)
	try:
		obs_json = json.loads(get_response.text)
		for k in obs_json:
			print k
			print obs_json[k]
	except:
		pass


def picture_request():
	# Ping shore computer
	schema = 'http://'; authority = '192.168.0.106';port='3333';teamCode='TUCE'
	course = ['courseA','courseB','openTest']
	active_course = course[1]
	pic_path = '/run/start/' + active_course + '/' + teamCode
	pic_url = schema + authority + ':' + port +  pic_path
	print 'sending request to '
	print start_url
	post_response = requests.post(start_url)
	if 'ERROR' in post_response.text:
		time.sleep(2)
	post_response = requests.post(start_url)


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
        frame = ''
	# Init obstacle course
	try:
		gate_request()
		pass
	except:
		pass
	# Try and download pictures 
	try:
		pass
	except:
		pass
        # Main loop
	while not rospy.is_shutdown():
		'''
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
		'''
                rate.sleep()

if __name__ == '__main__':
	main()

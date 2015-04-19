import time
import rospy
from team_software.msg import SuicideTask

def main():
	speed_pub = rospy.Publisher('SuicideTask',SuicideTask, queue_size=10)
        rospy.init_node('speednode')
        rate = rospy.Rate(10)
        suicide_msg = SuicideTask()
        suicide_msg.suicidetask = False
        counter = 0
	while not rospy.is_shutdown():
		print "Speed on"
		time.sleep(1)
                counter += 1
                speed_pub.publish(suicide_msg)
                if (counter == 5): suicide_msg.suicidetask = True

if __name__ == '__main__':
	main()

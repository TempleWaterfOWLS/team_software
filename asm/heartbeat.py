''' 
Code written to send heartbeat data from the boat to the shore computer
The heartbeat must send:
-Timestamp:  YYYYMMDDHHMMSS in UTC
-Challenge : 'gates','obstacles','docking,'pinger','interop','return'
-Position
  +datum: str
  +latitude: float 
  +longitude: float
Subscribes to task and nav fix
'''

# Imports
import requests; import json; import sys; import rospy
from time import strftime, sleep, gmtime, sleep

from team_software.msg import CurrentTask
curr_task = "speed"

def CurrentTask_Callback(data):
        global curr_task
        curr_task = data.currentTask

# Function designed to print information about the get response for debugging purposes
def print_response(get_response):
	print "URL Accesed"
	print get_response.url
	print "Status Code:"
	print get_response.status_code
	print "Headers:"
	print get_response.headers
	print "Text content:"
	print get_response.text
        return

def send_beat(url):
        rospy.init_node('heartnode')
        rate = rospy.Rate(10)
        # Continually send requests
        while not rospy.is_shutdown():
		print "Obtaining payload..."
		timestamp = strftime("%Y%m%d%H%M%S",gmtime())
		payload = {
			"timestamp":timestamp,
			"challenge":curr_task,
			"position" : {
				"datum": "WGS84",
				"latitude": 32.0,
				"longitude": 16.0,
				}
			   }
		print "Sending Request..."
		json_data = json.dumps(payload)
		print json_data
		print url
                #post_response = requests.post(url,data=json_data)
                # Print out useful debugging information about the request
                #print_response(post_response)
		sleep(1000)
                # Subscribe to thing
                rospy.Subscriber("CurrentTask", CurrentTask, CurrentTask_Callback)
                # Delay for next request
		rate.sleep()


# Call main boiler plate
if __name__ == '__main__':
	# Declare serverIP, port, and desired index to create URL
	serverIP = "192.168.0.100"; port="6666"; directory = "/heartbeat";
	course = "/courseA"; team_code = "/TUWF";
	directory += course + team_code
	url="http://"+serverIP+":"+port+directory

        send_beat(url)

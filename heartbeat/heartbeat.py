''' 
Code written to send heartbeat data from the boat to the shore computer
The heartbeat must send:
-Timestamp:  YYYYMMDDHHMMSS in UTC
-Challenge : 'gates','obstacles','docking,'pinger','interop','return'
-Position
  +datum: str
  +latitude: float 
  +longitude: float
'''
# Global gps_coords
gps_coords = [0,0]

# Imports
import requests; import json; import sys; import rospy
from time import strftime, sleep, gmtime
# Import messages we're listening to 
try:
        from team_software.msg import NavSatFix
except:
        pass
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
        # Ros subscription stuff
        rospy.init_node('heartbeat')
        rospy.rate(5)
        # Continually send requests
        while not rospy.is_shutdown():
		print "Obtaining payload..."
		timestamp = strftime("%Y%m%d%H%M%S",gmtime())
		payload = {
			"timestamp":timestamp,
			"challenge":"gates",
			"position" : {
				"datum": "TUWF",
				"latitude": gps_coords[0],
				"longitude": gps_coords[1],
				}
			   }
		print "Sending Request..."
		json_data = json.dumps(payload)
		print json_data
                post_response = requests.post(url,data=json_data)
                # Print out useful debugging information about the request
                print_response(post_response)
                # Delay for next request
              	print "Sleeping for 500ms"
		sleep(0.5)
                rospy.Subscriber("NavSatFix", NavSatFix, get_GPSfix, gps_coords)
                rate.sleep()

def get_GPSfix(data,gps_coords):
        global gps_coords
        gps_coords[0] = data.latitude
        gps_coords[1] = data.longitude


# Call main boiler plate
if __name__ == '__main__':
	# Declare serverIP, port, and desired index to create URL
	serverIP = "192.168.0.103"; port="80"; directory = "/heartbeat/";
	course = "/courseA/"; team_code = "/TUWF";
	directory += course + team_code
	url="http://"+serverIP+":"+port+directory
        send_beat(url)

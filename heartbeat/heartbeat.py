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
        # Continually send requests
        while True:
		print "Obtaining payload..."
		timestamp = strftime("%Y%m%d%H%M%S",gmtime())
		payload = {
			"timestamp":timestamp,
			"challenge":"gates",
			"position" : {
				"datum": "TUWF",
				"latitude": 32.0,
				"longitude": 16.0,
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


# Call main boiler plate
if __name__ == '__main__':
	# Declare serverIP, port, and desired index to create URL
	serverIP = "192.168.0.103"; port="80"; directory = "/heartbeat/";
	course = "/courseA/"; team_code = "/TUWF";
	directory += course + team_code
	url="http://"+serverIP+":"+port+directory
        send_beat(url)

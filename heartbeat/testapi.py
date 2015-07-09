'''
Program created to test API usage in roboboat competition
Made by Zack Smith 7-03-15
'''

import requests
import json
from time import sleep, gmtime, strftime

# Function designed to print information about the get response for debugging purposes
def print_response(get_response):
	print "URL Accesed:",
	print get_response.url
	#print "Status Code:"
	#print get_response.status_code
	#print "Headers:"
	#print get_response.headers
	print "Text content:"
	print get_response.text
        return

#POST on /run/start/<course>/<team Code>
# and /run/end/'''
def main():
    schema = 'http://'; authority = '0.0.0.0'; port = '3333';
    course = ['courseA','courseB', 'openTest']; teamCode = 'TUCE'
    active_course = course[0];
    # Construct URL
    heart_path = '/heartbeat/' +active_course+'/'+teamCode;
    heart_url = schema + authority + ':' + port + heart_path
    print heart_url
    heart_response = requests.post(heart_url)
    print_response(heart_response)
    x = json.loads(heart_response.text)
    print json.loads(heart_response.text)
    for keys in x:
        print keys
        print x[keys]

if __name__ == '__main__':
    main()

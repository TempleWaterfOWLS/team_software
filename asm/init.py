'''
Program created to test API usage in roboboat competition
Made by Zack Smith 7-03-15
'''

import requests
import json
from time import sleep, gmtime, strftime

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
        print 'TIMESTAMPS'
        print strftime("%Y-%m-%d %H:%M:%S")
        return

#POST on /run/start/<course>/<team Code>
# and /run/end/'''
def main():
    schema = 'http://'; authority = 'ec2-52-7-253-202.compute-1.amazonaws.com'; port = 80;
    course = ['courseA','courseB', 'openTest']; teamCode = 'TUCE'
    active_course = course[1];
    # Construct URL
    start_path = '/run/start/' +active_course+'/'+teamCode;
    end_path = '/run/end/' + active_course + '/' + teamCode;
    start_url = schema + authority + start_path
    end_url = schema + authority + end_path
    print start_url
    response = "ERROR"
    #print end_url
    # Start and stop a run
    x = 0
    while "ERROR" in response:
            post_response = requests.post(start_url)
            response = post_response.text
            print_response(post_response)
            active_course = course[x]
            x = x+1
            if (x == 3): x = 0
            start_path = '/run/start/' +active_course+'/'+teamCode;
            start_url = schema + authority + start_path
            sleep(2)
    post_response = requests.post(end_url)
    print_response(post_response)
    # Test get request
    get_url = schema + authority + '/ping'
    get_response = requests.get(get_url)
    print_response(get_response)
    # Interop challenge
    #interop_url = schema + authority + '/interop/images/' + active_course + '/' + 'TUWF'
    #interop_response = requests.get(interop_url)
    #print_response(interop_response)

if __name__ == '__main__':
    main()

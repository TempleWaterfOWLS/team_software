'''
Program created to test API usage in roboboat competition
Made by Zack Smith 7-03-15
'''
# Libraries for making and formatting HTML requests
import requests
import json
# Library for parsing of HTML heirarchy
from bs4 import BeautifulSoup as Soup, Tag
# Library for being a time warlock
from time import sleep, gmtime, strftime

def download_img(get_response,filename):
    '''
    Function to download image given the response of the img URL    
    '''
    print 'Downloading ' + filename
    if get_response.status_code == 200:
        with open(filename,'wb') as f:
            for chunk in get_response:
                f.write(chunk)
    #print 'Finished downloading'

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
    schema = 'http://'; authority = 'ec2-52-7-253-202.compute-1.amazonaws.com'; port = 80;
    course = ['courseA','courseB', 'openTest']; teamCode = 'TUCE'
    directories = ['ec2-54-210-13-60.compute-1.amazonaws.com', 'ec2-52-7-253-202.compute-1.amazonaws.com']
    active_course = course[0];
    # Construct URL
    start_path = '/run/start/' +active_course+'/'+teamCode;
    end_path = '/run/end/' + active_course + '/' + teamCode;
    start_url = schema + authority + start_path
    end_url = schema + authority + end_path
    response = "ERROR"
    # print end_url
    # Start and stop a run
    # Test get request
    get_url = schema + authority + '/ping'
    get_response = requests.get(get_url)
    print_response(get_response)
    x = 0
    while 1: # Keep trying to connect while error
        start = True; hard_code = True
        active_course = 'courseB'; authority = directories[0]
        if 'ERROR' in response and not hard_code:
            active_course = course[x]
            if (start):
                start_path = '/run/start/' +active_course+'/'+teamCode;        
                start_url = schema + authority + start_path
                post_response = requests.post(start_url)
                response = post_response.text
                print_response(post_response)
            else:
                end_path = '/run/end/' + active_course + '/' + teamCode;
                end_url = schema + authority + end_path
                post_response = requests.post(end_url)
                response = post_response.text
                print_response(post_response)

            x = x + 1; 
            if (x==3): 
                x=0                
                if (authority == directories[0]): authority = directories[1]
                else: authority = directories[0]
        else:
            ### OBSTACLE REQUEST
            obstacle_url = schema + authority + '/obstacleAvoidance/' + active_course + '/' + teamCode
            obs_response = requests.get(obstacle_url)
            print_response(obs_response)
            obs_json = json.loads(obs_response.text)
            print obs_json
            # print out the keys
            print '!!!!!!!!!!!!!! OBS DICT !!!!!!!!!!!!!!!!!!'
            for k in obs_json:
                    print k

            ### DOCKING REQUEST
            docking_url = schema + authority + '/automatedDocking/' + active_course + '/' + teamCode
            docking_response = requests.get(docking_url)
            print_response(docking_response)
            dock_json = json.loads(docking_response.text)
            print '!!!!!!!!!!!!!! DOCK DICT !!!!!!!!!!!!!!!!'
            for k in dock_json:
                    print k
            ### PINGER REQUEST
            ping_url = schema + authority + '/pinger/' + active_course + '/' + teamCode
            # format json payload
            payload = {
                    "course":active_course,
                    "team":teamCode,
                    "buoyColor":"green"
                }
            json_data = json.dumps(payload)
            json_headers={"content-type": "application/json"}
            ping_response = requests.post(ping_url,data=json_data,headers=json_headers)
            print_response(ping_response)
            ping_json = json.loads(ping_response.text)
            print '!!!!!!!!!!!!!!!!!! PING DICT !!!!!!!!!!!!!!'
            for k in ping_json:
                    print k
            ### INTEROP REQUESTS
            ## Get images
            interop_url = schema + authority + '/interop/images/' + active_course + '/' + teamCode
            interop_response = requests.get(interop_url)
            #print_response(interop_response)
            # Time for code I stole from stackoverflow
            soup = Soup(interop_response.text)

            img_ul = soup.findAll('li')
            for item in img_ul:
                if isinstance(item,Tag):
                        #print item.text
                        if (item.text[0] != '.' and not item.text.endswith('.tiff')):
                                img_url = schema + authority + '/interop/' + 'image/' + active_course + '/' + teamCode + '/' + item.text
                                #print img_url
                                img_resp = requests.get(img_url, stream=True)
                                download_img(img_resp,item.text)
            # Send image for request
            interop_url = schema + authority + '/interop/image/' + active_course + '/' + teamCode
            img_header = {"content-type":"multipart/mixed"}
            interop_response = requests.post(interop_url,files={'0.jpg': open('0.jpg', 'rb')})
            print_response(interop_response)
            #inter_json = json.loads(interop_response.text)
            #print '!!!!!!!!!!!!!!! INTEROP DICT !!!!!!!!!!!'
            #for k in inter_json:
            #        print k
            ### HEARTBEAT REQUESTS
            tstamp = strftime("%Y%m%d%H%M%S")
            hpayload = {
                    "timestamp": tstamp,
                    "challenge": "gates",
                    "position": {
                            "datum": "WGS84",
                            "latitude": 34.4,
                            "longitude": 28.6
                            }
                }            
            hbeat_url = schema + authority + '/heartbeat/' + active_course + '/' + teamCode            
            hbeat_request = requests.post(hbeat_url,data=json.dumps(hpayload),headers=json_headers)
            print_response(hbeat_request)

            while 1:
                pass
             

    # End run
    post_response = requests.post(end_url)
    print_response(post_response)

if __name__ == '__main__':
    main()

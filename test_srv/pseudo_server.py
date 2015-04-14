2#import the HTTP libraries
import httplib
from BaseHTTPServer import BaseHTTPRequestHandler
from flask import * #Flask, render_template, request, url_for
import cgi 

# Global Status Variables

OK = 200
MALFORMED = 400
ERROR = 404
GATE_BROKEN = 500
RETRY = 503

# When posting, the client must specify the client address/URL



#1) Supporting the HeartBeat POST requests
# Note for the heartbeat, the post should be made on /heartbeat/
# Edit the path to /heartbeat/ to accomplish this

# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates

app = Flask(__name__)

@app.route('/')
def form():
    return 'TEST '#render_template('form_submit.html')


#6.2 HEARTBEAT RESPONSE
@app.route('/heartbeat/<course>/<teamCode>', methods=['GET','POST'])
def heartbeat(course, teamCode):
    response = jsonify(success = True)
    # make_response(render_template('heartbeat_response.html', status = '200'))
    # response.headers['HEADER'] = 'HEADER'
    return response 

#5.5 UAV
@app.route('/interop/report/<course>/<teamCode>', methods=['GET','POST'])
def uav(course, teamCode):
    response = jsonify(success = True)
    # make_response(render_template('uav_response.html', status = '200'))
    # response.headers['HEADER'] = 'HEADER'
    return response 

#5.4 PINGER
@app.route('/pinger/<course>/<teamCode>', methods=['GET','POST'])
def pinger(course, teamCode):
    response = jsonify(success = True)
    # make_response(render_template('pinger_response.html', status = '200'))
    # response.headers['HEADER'] = 'HEADER'
    return response 

#5.3 AUTOMATED DOCKING
@app.route('/automatedDocking/<course>/<teamCode>', methods=['GET','POST'])
def docking(course, teamCode):
    
    response = jsonify(success = True, dockingBaySequence = True )
    # make_response(render_template('docking_response.html', status = '200'))
    # response.headers['HEADER'] = 'HEADER'
    return response 


#5.2 OBSTACLE AVOIDANCE
@app.route('/obstacleAvoidance/<course>/<teamCode>', methods=['GET','POST'])
def obstacle(course, teamCode):
    response = jsonify(success = True, gateCode = {'1','Z'})
    # make_response(render_template('obstacle_response.html', status = '200'))
    # response.headers['HEADER'] = 'HEADER'
    return response 



if __name__ == '__main__':
    app.run(debug=True)

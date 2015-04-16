from flask import * #Flask, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def form():
    return 'TEST '

#6.2 HEARTBEAT RESPONSE
@app.route('/heartbeat/<course>/<teamCode>', methods=['GET','POST'])
def heartbeat(course, teamCode):
    response = jsonify(success = True)
    return response 

#5.5 UAV
@app.route('/interop/report/<course>/<teamCode>', methods=['GET','POST'])
def uav(course, teamCode):
    response = jsonify(success = True)
    return response 

#5.4 PINGER
@app.route('/pinger/<course>/<teamCode>', methods=['GET','POST'])
def pinger(course, teamCode):
    response = jsonify(success = True)
    return response 

#5.3 AUTOMATED DOCKING
@app.route('/automatedDocking/<course>/<teamCode>', methods=['GET','POST'])
def docking(course, teamCode):
    response = jsonify(success = True, dockingBaySequence = True )
    return response 

#5.2 OBSTACLE AVOIDANCE
@app.route('/obstacleAvoidance/<course>/<teamCode>', methods=['GET','POST'])
def obstacle(course, teamCode):
    response = jsonify(success = True, gateCode = {'1','Z'})
    return response 

if __name__ == '__main__':
    app.run(debug=True)

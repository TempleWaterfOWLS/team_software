from flask import * 

app = Flask(__name__)

@app.route('/')
def form():
    return 'Psuedo Srv Landing Page'

#6.3 STARTING RUN
@app.route('/run/start/<course>/<teamCode>', methods=['GET','POST'])
def start_run(course,teamCode):
    response = jsonify(success=True)
    return response

#6.3 ENDING RUN
@app.route('/run/end/<course>/<teamCode>',methods=['GET','POST'])
    response = jsonify(success=True)
    return response

#6.2 HEARTBEAT RESPONSE
@app.route('/heartbeat/<course>/<teamCode>', methods=['GET','POST'])
def heartbeat(course, teamCode):
    response = jsonify(success = True)
    return response 

# 5.5 UAV
# Upload Image
# Request - Multipart/mixed
@app.route('/interop/image/<course>/<teamCode>', methods=['GET','POST'])
def uav(course, teamCode):
    response = jsonify(id='yoloswagupload420')
    return response 

# Reporting shape 
# Request - course:<course> team:<teamcode> shape: <shape> image: <imageID>
@app.route('/interop/report/<course>/<teamCode>', methods=['GET','POST'])
def uav_report(course, teamCode):
    response = jsonify(success = True)
    return response 

#5.4 PINGER
# Report Pinger
# Request - course: <course> team: <teamcode> buoycolor: buoycolor
@app.route('/pinger/<course>/<teamCode>', methods=['GET','POST'])
def pinger(course, teamCode):
    response = jsonify(success = True)
    return response 

#5.3 AUTOMATED DOCKING
# For grabbing sequence info etc
# Request - GET on URL
@app.route('/automatedDocking/<course>/<teamCode>', methods=['GET','POST'])
def docking(course, teamCode):
    res = [ {'symbol':'triangle','color':'blue'},   {'symbol':'square','color':'red'}] 
    response = jsonify(dockingBaySequence = res)
    return response 

#5.2 OBSTACLE AVOIDANCE
# For getting starting gate info etc
# Request - GET on URL
@app.route('/obstacleAvoidance/<course>/<teamCode>', methods=['GET','POST'])
def obstacle(course, teamCode):
    response = jsonify(gateCode = ['1','Z'])
    return response 

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3333,debug=True)

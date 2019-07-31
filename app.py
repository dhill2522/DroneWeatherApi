from flask import Flask, request, Response
from flask_cors import CORS
import drone_awe
import json
import utilities

'''
Notes:
    - Need to disable plotting in the library
    - if possible remove matplotlib entirely from the library
    - if possible remove gekko object from a.output in order to make it JSONSerializable
'''

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return json.dumps({
        'msg': 'Drones and weather API 0.0.2. See DroneEcon.com for details.'
    })

@app.route('/getValidationCases')
def getValidationCases():
    try:
        a = drone_awe.model({})
        data = a.getValidationCases()
        data = [d for d in data if 'xvalid' in d]
        resp = Response(json.dumps(data))
        return resp
    except Exception as err:
        return utilities.handleError(err)

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        params = {}
        if request.data:
            params = json.loads(request.data)

        for arg in utilities.defaultArgs:
            if arg['name'] not in params:
                print('Missing parameters', arg['name'], '. Using default:', arg['default'])
                params[arg['name']] = arg['default']
            
        a = drone_awe.model(params)
        data = a.simulate()
        resp = Response(json.dumps(data))
        return resp
    except Exception as err:
        return utilities.handleError(err)

app.run()


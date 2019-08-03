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
        data = drone_awe.validationdatabase
        data = [d for d in data if 'xvalid' in d]
        resp = Response(json.dumps(data))
        return resp
    except Exception as err:
        return utilities.handleError(err)

@app.route('/getDrones')
def getDrones():
    try:
        return Response(json.dumps(drone_awe.drones))
    except Exception as err:
        utilities.handleError(err)
    a.simulate()


@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        # Track Z-variable
        zParam = None

        params = {}
        if request.data:
            params = json.loads(request.data)
            # zParam = params['zParam']

        for arg in utilities.DefaultArgs:
            if arg['name'] not in params:
                print('Missing parameters', arg['name'], '. Using default:', arg['default'])
                params[arg['name']] = arg['default']
            
        a = drone_awe.model(params)
        a.simulate()
        data = a.output

        resp = {
            'plottables': [],
            'zAxis': {
                'id': zParam,
                'displayName': '',
                'values': []
            }
        }

        if zParam:
            resp['zAxis']['displayName'] = data['zvals']

        for key in list(data.keys()):
            if type(data[key][0]) != str and key != 'zvals':
                l = list(filter(lambda el: el['param'] == key, utilities.ParamMap))

                if len(l) >= 1:
                    displayName = l[0]['display']
                    plottable = {
                        'id': key,
                        'displayName': displayName,
                        'values': data[key] 
                    }
                    resp['plottables'].append(plottable)
                else:
                    print(f'Missing ParamMep entry for {key}')
        resp = Response(json.dumps(resp))
        return resp
    except Exception as err:
        return utilities.handleError(err)

app.run()


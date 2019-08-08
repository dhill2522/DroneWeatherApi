from flask import Flask, request, Response
from flask_cors import CORS
import drone_awe
import json
import copy
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
        drones = copy.deepcopy(drone_awe.drones)
        resp = []
        for drone in drones:
            el = {}
            if 'battery' in drone:
                for prop in drone['battery']:
                    l = list(filter(lambda el: el['param'] == prop, utilities.ParamMap))
                    if len(l) > 0:
                        el[l[0]['display']] = drone['battery'][prop]
                del drone['battery']
            for prop in drone:
                l = list(filter(lambda el: el['param'] == prop, utilities.ParamMap))
                if len(l) > 0:
                    el[l[0]['display']] = drone[prop]
            resp.append(el)
                
        return Response(json.dumps(resp))
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
                print(f'Missing', {arg['name']}, 'Using default value:', {arg['default']})
                params[arg['name']] = arg['default']
            
        a = drone_awe.model(params)
        a.simulate()
        data = a.output

        resp = {
            'error': False,
            'errorType': None,
            'log': a.outputlog,
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
            if key != 'zvals' and type(data[key][0][0]) != str:
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


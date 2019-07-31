from flask import Response
import traceback

defaultArgs = [
    { 'name': 'validation', 'default': True },
    { 'name': 'validationcase', 'default': 'DiFranco2016' },
    { 'name': 'dronename', 'default': 'dji-Mavic2' },
    { 'name': 'batterytechnology', 'default': 'near-future'},
    { 'name': 'stateofhealth', 'default': 90.0 },
    { 'name': 'startstateofcharge', 'default': 100.0 },
    { 'name': 'altitude', 'default': 100.0 },
    { 'name': 'dropsize', 'default': 1.0 },
    { 'name': 'liquidwatercontent', 'default': 1.0 },
    { 'name': 'temperature', 'default': 15.0 },
    { 'name': 'windspeed', 'default': 10.0 },
    { 'name': 'winddirection', 'default': 0.0 },
    { 'name': 'relativehumidity', 'default': 0.0 },
    { 'name': 'timestep', 'default': 1 },
    { 'name': 'plot', 'default': False },
    { 'name': 'xlabel', 'default': "missionspeed" },
    { 'name': 'ylabel', 'default': "power" },
    { 'name': 'title', 'default': "First_test" },
    { 'name': 'simulationtype', 'default': "simple" },
    { 'name': 'weathereffect', 'default': "temperature" }
]

def handleError(err: Exception):
    print('Internal Error')
    print(err, type(err))
    traceback.print_tb(err.__traceback__)
    msg = {
        'error': True,
        'msg': 'An internal error has occured'
    }
    resp = Response(json.dumps(msg))
    return resp
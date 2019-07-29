from flask import Flask, request
import drone_awe
import jsonpickle

'''
Notes:
    - Need to disable plotting in the library
    - if possible remove matplotlib entirely from the library
    - if possible remove gekko object from a.output in order to make it JSONSerializable
'''

app = Flask(__name__)

@app.route('/')
def root():
    return 'Hello World!'

@app.route('/simulate', methods=['POST'])
def run_simulation():
    try:
        print(request.form)
        params = {
            "validation":True,
            "validationcase":"DiFranco2016",
            "drone":True,
            "dronename":"dji-Mavic2",
            "batterytechnology":"near-future",
            "stateofhealth":90.0,
            "startstateofcharge":100.0,
            "altitude":100.0,
            "rain":False,
            "dropsize":1.0,
            "liquidwatercontent":1.0,
            "temperature":15.0,
            "wind":False,
            "windspeed":10.0,
            "winddirection":0.0,
            "relativehumidity":0.0,
            "icing":False,
            "timestep":1,
            "plot":True,
            "xlabel":"missionspeed",
            "ylabel":"power",
            "title":"First_test",
            "simulationtype":"simple",
            "model":"abdilla",
            "xbegin":0,
            "xend":1,
            "xnumber":5,
            "weathereffect":"temperature",
            "weatherbegin":10,
            "weatherend":40,
            "weathernumber":3
        }

        a = drone_awe.drone_awe(params)
        data = a.simulate()
        return jsonpickle.encode(data)
    except Exception as err:
        print('Internal Error:')
        print(err)
        msg = {
            'error': True,
            'msg': 'An internal error has occured'
        }
        return jsonpickle.encode(msg)

app.run()


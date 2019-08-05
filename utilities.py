from flask import Response
import json
import traceback

DefaultArgs = [
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

ParamMap = [
    { 'param': 'id', 'display': 'Drone Name' },
    { 'param': 'wingtype', 'display': 'Wing Type' },
    { 'param': 'diagonal', 'display': 'Diagonal (m)' },
    { 'param': 'takeoffweight', 'display': 'Takoff Weight (kg)' },
    { 'param': 'speedmax', 'display': 'Max Speed (m/s)' },
    { 'param': 'altitudemax', 'display': 'Max Altitude (m)' },
    { 'param': 'endurancemax', 'display': 'Max Endurance (min)' },
    { 'param': 'endurancemaxspeed', 'display': 'Max Endurace Speed (m/s)' },
    { 'param': 'endurancemaxhover', 'display': 'Max Hover Endurance (min)' },
    { 'param': 'rangemax', 'display': 'Max Range (m)' },
    { 'param': 'rangemaxspeed', 'display': 'Max Range Speed (m/s)' },
    { 'param': 'tiltanglemax', 'display': 'Max Tilt Angle (degrees)' },
    { 'param': 'temperaturemin', 'display': 'Min Temperature (C)' },
    { 'param': 'chargerpowerrating', 'display': 'Charger Power Rating (W)' },
    { 'param': 'batterytype', 'display': 'Battery Type' },
    { 'param': 'batterycapacity', 'display': 'Battery Capacity (mA-h)' },
    { 'param': 'batteryvoltage', 'display': 'Battery Voltage (V)' },
    { 'param': 'batterycells', 'display': 'Battery Cell Count' },
    { 'param': 'batteryenergy', 'display': 'Battery Energy (J)' },
    { 'param': 'batterymass', 'display': 'Battery Mass (kg)' },
    { 'param': 'waterproof', 'display': 'Waterproof' },
    { 'param': 'windspeedmax', 'display': 'Max Windspeed (m/s)' },
    { 'param': 'batteryrechargetime', 'display': 'Battery Recharge Time (min)' },
    { 'param': 'rotorquantity', 'display': 'Rotor Quantity' },
    { 'param': 'rotordiameter', 'display': 'Rotor Diameter (m)' },
    { 'param': 'cruisespeed', 'display': 'Cruise Speed (m/s)' },
    { 'param': 'payload', 'display': 'Payload (kg)' },
    { 'param': 'length', 'display': 'Length (m)' },
    { 'param': 'width', 'display': 'Width (m)' },
    { 'param': 'height', 'display': 'Height (m)' },
    { 'param': 'frontalarea', 'display': 'Frontal Area (m²)' },
    { 'param': 'toparea', 'display': 'Top Area (m²)' },
    { 'param': 'endurancemaxrange', 'display': 'Max Edurance Range (m)' },
    { 'param': 'rotorarea', 'display': 'Rotor Area (m²)' },
    # { 'param': 'totalweight', 'display': 'Total Weight (kg)' },
    { 'param': 'capacity', 'display': 'Capacity (A-h)' },
    { 'param': 'soc', 'display': 'State of Charge (%)' },
    { 'param': 'startsoc', 'display': 'Initial State of Charge (%)' },
    { 'param': 'soh', 'display': 'State of Health (%)' },
    { 'param': 'voltage', 'display': 'Voltage (V)' },
    { 'param': 'voltagemean', 'display': 'Mean Voltage (V)' },
    { 'param': 'voltagecharged', 'display': 'Charged Voltage (V)' },
    { 'param': 'voltagedead', 'display': 'Dead Voltage (V)' },
    { 'param': 'current', 'display': 'Current (A)' },
    { 'param': 'batterytechnology', 'display': 'Battery Technology' },
    { 'param': 'efficiencypropulsive', 'display': 'Propulsive Efficiency' },
    { 'param': 'power', 'display': 'Power (W)' },
    { 'param': 'dragcoefficient', 'display': 'Drag Coefficient' },
    { 'param': 'alpha', 'display': 'Alpha (degrees)' },
    { 'param': 'area', 'display': 'Area (m²)' },
    { 'param': 'velocityinducedhover', 'display': 'Rotor Induced Velocity (hover) (m/s)' },
    { 'param': 'velocityinduced', 'display': 'Induced Velocity (m/s)' },
    { 'param': 'thrust', 'display': 'Thrust (N)' },
    { 'param': 'alpha_gekko', 'display': 'Alpha (Gekko) (radians)' },
    { 'param': 'drag', 'display': 'Drag (N)' },
    { 'param': 'bladeprofilepower', 'display': 'Blade Power Profile' },
    { 'param': 'airdensity', 'display': 'Air Density (kg/m³)' },
    { 'param': 'airdensitysealevel', 'display': 'Air Density At Sea Level (kg/m³)' },
    { 'param': 'gravitationconstant', 'display': 'Gravitational Constant (m/s²)' },
    { 'param': 'temperaturesealevel', 'display': 'Temperature At Sea Level (C)' },
    { 'param': 'temperature', 'display': 'Temperature (C)' },
    { 'param': 'humidity', 'display': 'Humidity (g/m³)' },
    { 'param': 'altitude', 'display': 'Altitude (m)' },
    { 'param': 'relativehumidity', 'display': 'Relative Humidity (%)' },
    { 'param': 'missionspeed', 'display': 'Mission Speed (m/s)' },
    { 'param': 'heading', 'display': 'Heading (degrees)' },
    { 'param': 'simulationtype', 'display': 'Simulation Type' },
    { 'param': 'timestep', 'display': 'Time Step (s)' },
    { 'param': 'clock', 'display': 'Clock (s)' },
    { 'param': 'counter', 'display': 'Counter' },
    { 'param': 'range', 'display': 'Range (m)' },
    { 'param': 'endurance', 'display': 'Endurance (min)' },
]

def handleError(err: Exception):
    print('Internal Error')
    print(err, type(err))
    traceback.print_tb(err.__traceback__)
    msg = {
        'error': True,
        'errorType': type(err),
        'log': err.__repr__()
    }
    try:
        resp = Response(json.dumps(msg))
    except:
        msg = {
            'error': True,
            'errorType': 'Error',
            'log': 'Internal Server Error'
        }
        resp = Response(json.dumps(msg))
    return resp
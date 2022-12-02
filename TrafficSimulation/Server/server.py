# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
'''
Gerardo Gutiérrez Paniagua, A01029422
Mateo Herrera Lavalle A01751912
Francisco Daniel Salcedo Catalán A01633010
Regina Rodríguez Sánchez A01284329
'''
# Novimebre 2022
# Octavio Navarro. October 2021

# Python Server for Unity visualization

from flask import Flask, request, jsonify
from trafficAgents import *

# Size of the board and number of agents:
number_agents = 10
width = 28
height = 28
randomModel = None
currentStep = 0

app = Flask("Traffic example")

# @app.route('/', methods=['POST', 'GET'])

# init endpoint for map dimensions
@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel, number_agents

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        # width = int(request.form.get('width'))
        # height = int(request.form.get('height'))
        currentStep = 0

        randomModel = RandomModel(number_agents)

        return jsonify({"message":"Parameters received, model initiated."})

# GET endpoint of the positions of agents
@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
        agentPositions = [{"id": str(agent.unique_id), "x": x, "y":0, "z":z, "arrived": agent.arrived} for (contents, x, z) in randomModel.grid.coord_iter() for agent in contents if isinstance(agent, Car)]

        return jsonify({'positions':agentPositions})

# GET endpoint for traffic light states, red or green
@app.route('/getTrafficLight', methods=['GET'])
def getTrafficLight():
    global randomModel
    if request.method == 'GET':
        tLightsState = [{"id": str(t.unique_id), "x": t.pos[0], "y":0, "z":t.pos[1], "state": t.state} for t in randomModel.traffic_lights]

        return jsonify({'tLightsState':tLightsState})

#GET endpoint for step updates in the model
@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

# run server on localhost, port 8585
if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)
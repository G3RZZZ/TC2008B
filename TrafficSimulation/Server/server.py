# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2021

from flask import Flask, request, jsonify
from trafficAgents import *

# Size of the board:
number_agents = 10
width = 28
height = 28
randomModel = None
currentStep = 0

app = Flask("Traffic example")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel, number_agents, width, height

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        currentStep = 0

        randomModel = RandomModel(number_agents)

        return jsonify({"message":"Parameters received, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
        agentPositions = [{"id": str(agent.unique_id), "x": x, "y":0, "z":z, "arrived": agent.arrived} for (contents, x, z) in randomModel.grid.coord_iter() for agent in contents if isinstance(agent, Car)]

        return jsonify({'positions':agentPositions})

@app.route('/getTrafficLight', methods=['GET'])
def getTrafficLight():
    global randomModel
    if request.method == 'GET':
        tLightsState = [{"id": str(t.unique_id), "x": t.pos[0], "y":0, "z":t.pos[1], "state": t.state} for t in randomModel.traffic_lights]

        return jsonify({'tLightsState':tLightsState})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)
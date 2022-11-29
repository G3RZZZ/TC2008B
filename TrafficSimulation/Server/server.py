# # Mateo Herrera - A01751912
# Gerardo Gutierrez - A01029422
# Francisco Salcedo -  A01633010
# Regina Rodriguez - A01284329

from flask import Flask, request, jsonify
from trafficAgents import *


agents = None
N = 5
currentStep = 0
width = 0
height = 0

app = Flask("Traffic Simulation")

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel, agents, width, height, N

    if request.method == 'POST':
        # width = int(request.form.get('width'))
        # height = int(request.form.get('height'))
        currentStep = 0
        agents = agents(N)

        randomModel = RandomModel(N)

        return jsonify({"message":"Parameters received, model initiated"})


@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
        agentPositions = [{"id": str(agent.unique_id), "x": x, "y":0, "z":z, "steps_taken": agent.steps_taken, "xl": agent.look_here[0], "zl": agent.look_here[1]} for (contents, x, z) in randomModel.grid.coord_iter() for agent in contents if isinstance(agent, Car)]

        print(len(agentPositions))

        return jsonify({'positions':agentPositions})


@app.route('/getObstacles', methods=['GET'])
def getObstacles():
    global randomModel

    if request.method == 'GET':
        obstaclePositions = [{"id": str(agent.unique_id), "x": x, "y":0, "z":z} for (contents, x, z) in randomModel.grid.coord_iter() for agent in contents if isinstance(agent, Obstacle)]

        return jsonify({'positions':obstaclePositions})

@app.route('/getTraffic_Light', methods=['GET'])
def getTowers():
    global randomModel

    if request.method == 'GET':
        tLightPositions = [{"id": str(agent.unique_id), "x": x, "y":0, "z":z} for (contents, x, z) in randomModel.grid.coord_iter() for agent in contents if isinstance(agent, Traffic_Light)]

        return jsonify({'positions':tLightPositions})

@app.route('/getRoad', methods=['GET'])
def getRoad():
    global randomModel

    if request.method == 'GET':
        roadPositions = [{"id": str(agent.unique_id), "x": x, "y":0.075, "z":z} for (contents, x, z) in randomModel.grid.coord_iter() for agent in contents if isinstance(agent, Road)]

        return jsonify({'positions':roadPositions})


@app.route('/getDestination', methods=['GET'])
def getDestination():
    global randomModel

    if request.method == 'GET':
        destinationPositions = [{"id": str(agent.unique_id), "x": x, "y":0, "z":z} for (contents, x, z) in randomModel.grid.coord_iter() for agent in contents if isinstance(agent, Destination)]

        return jsonify({'positions':destinationPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep, 'running': randomModel.running})


if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)


with open('2022_base.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)


print(width, height)

                       
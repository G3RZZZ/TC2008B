# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2021

from flask import Flask, request, jsonify
from RandomAgents import *

# Size of the board:
num_agents = 10
width = 28
height = 28
randomModel = None
currentStep = 0

app = Flask("Traffic example")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel, num_agents, width, height, num_towers

    if request.method == 'POST':
        num_agents = int(request.form.get('NAgents'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        num_towers = int(request.form.get('NTowers'))
        currentStep = 0

        print(request.form)
        print(num_agents, width, height)
        randomModel = RandomModel(num_agents, num_towers, width, height)

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
        agentPositions = [{"id": str(agent.unique_id), "x": x, "y":1, "z":z, "steps_taken": agent.steps_taken, "xl": agent.look_here[0], "zl": agent.look_here[1]} for (contents, x, z) in randomModel.grid.coord_iter() for agent in contents if isinstance(agent, RobotAgent)]

        print(len(agentPositions))

        return jsonify({'positions':agentPositions})

@app.route('/getObstacles', methods=['GET'])
def getObstacles():
    global randomModel

    if request.method == 'GET':
        carPositions = [{"id": str(agent.unique_id), "x": x, "y":1, "z":z} for (contents, x, z) in randomModel.grid.coord_iter() for agent in contents if isinstance(agent, ObstacleAgent)]

        return jsonify({'positions':carPositions})

@app.route('/getBoxes', methods=['GET'])
def getBoxes():
    global randomModel

    if request.method == 'GET':
        boxPositions = [{"id": str(agent.unique_id), "x": x, "y":1, "z":z} for (contents, x, z) in randomModel.grid.coord_iter() for agent in contents if isinstance(agent, BoxAgent)]

        return jsonify({'positions':boxPositions})

@app.route('/getTowers', methods=['GET'])
def getTowers():
    global randomModel

    if request.method == 'GET':
        towerPositions = [{"id": str(agent.unique_id), "x": x, "y":1, "z":z} for (contents, x, z) in randomModel.grid.coord_iter() for agent in contents if isinstance(agent, TowerAgent)]

        return jsonify({'positions':towerPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep, 'running': randomModel.running})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)
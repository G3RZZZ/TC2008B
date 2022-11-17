# Mateo Herrera Lavalle - A01751912
# Gerardo Gutierrez Paniagua - A01029422

from flask import Flask, request, jsonify
from RobotAgent import *

# Board
number_agents = 2
number_towers = 8
width = 10
height = 10
randomModel = None
currentStep = 0

app = Flask("Pick-up Box Bot")

@app.route('/init', mehtods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel, number_agents, width, height

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        number_towers = int(request.form.get('TAgents'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        currentStep = 0

        print(request.form)
        print(number_agents, width, height)
        randomModel = RandomModel(number_agents, number_towers, width, height)

        return jsonify({"message": "Parameters received, model initiated"})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
        agentPositions = [{"id": str(a.unique_id), "x": x, "y": 1, "z": z} for (a, x, z) in randomModel.grid.coord_iter() if isinstance(a, RobotAgent)]

        return jsonify({'positions': agentPositions})

@app.route('/getTowers', methods=['GET'])
def getTowers():
    global randomModel

    if request.method == 'GET':
        towerPositions = [{"id": str(a.unique_id), "x": x, "y": 1, "z": z} for (a, x, z) in randomModel.grid.coord_iter() if isinstance(a, TowerAgent)]

        return jsonify({'positions': towerPositions})

@app.route('/getObstacles', methods=['GET'])
def getObstacles():
    global randomModel

    if request.method == 'GET':
        obstaclePositions = [{"id": str(a.unique_id), "x": x, "y":1, "z":z} for (a, x, z) in randomModel.grid.coord_iter() if isinstance(a, ObstacleAgent)]

        return jsonify({'positions':obstaclePositions})

@app.route('/getBoxes', methods=['GET'])
def getBoxes():
    global randomModel

    if request.method == 'GET':
        BoxPositions = [{"id": str(a.unique_id), "x": x, "y": 1, "z": z} for (a, x, z) in randomModel.grid.coord_iter() if isinstance(a, BoxAgent)]

        return jsonify({'positions': BoxPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel

    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)
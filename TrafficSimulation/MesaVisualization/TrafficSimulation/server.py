# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
'''
Gerardo Gutiérrez Paniagua, A01029422
Mateo Herrera Lavalle A01751912
Francisco Daniel Salcedo Catalán A01633010
Regina Rodríguez Sánchez A01284329
'''
# Novimebre 2022
# Octavio Navarro. October 2021

# Python Server for Mesa web visualization

from agent import *
from model import RandomModel
from mesa.visualization.modules import CanvasGrid, BarChartModule
from mesa.visualization.ModularVisualization import ModularServer


# Definition of agent visuals, color, layer position, and size.
def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "Layer": 1,
                 "w": 1,
                 "h": 1
                 }

    if (isinstance(agent, Road)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
    
    if (isinstance(agent, Car)):
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
    
    if (isinstance(agent, Destination)):
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0

    if (isinstance(agent, Traffic_Light)):
        portrayal["Color"] = "red" if not agent.state else "green"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    if (isinstance(agent, Obstacle)):
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    return portrayal

# dimensions of the map
width = 0
height = 0

# Test file containing the map
with open('2022_base.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

model_params = {"N":5}

# Grid generation
print(width, height)
grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

# Server on localhost, port 8521
server = ModularServer(RandomModel, [grid], "Traffic Base", model_params)                       
server.port = 8521 # The default
server.launch()
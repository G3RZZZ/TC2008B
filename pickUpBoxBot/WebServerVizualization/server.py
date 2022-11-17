# Mateo Herrera Lavalle - A01751912
# Gerardo Gutierrez Paniagua - A01029422

from model import RandomModel, ObstacleAgent, BoxAgent, TowerAgent
from mesa.visualization.modules import CanvasGrid, BarChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import NumberInput, Slider


# Inicializar agentes con diferentes especificaciones dependiendo del tipo
def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    if (isinstance(agent, BoxAgent)):
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    
    if (isinstance(agent, TowerAgent)):
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.5

    return portrayal

# Pedir el width y el height al usuario
print("Enter the grid width: ")
width = int(input())
print("Enter the grid heigth: ")
heigth = int(input())

# Establecer parametros del modelo
model_params = {"N":NumberInput("Agent Number", 10), "width": width, "height": heigth, "density": Slider("Box density", 0.1, 0.01, 1, 0.01), "num_towers": NumberInput("TowerNumber", 1)}
grid = CanvasGrid(agent_portrayal, width, heigth, 500, 500)


# Crear server
server = ModularServer(RandomModel, [grid], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()
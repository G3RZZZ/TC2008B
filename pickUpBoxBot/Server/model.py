# Mateo Herrera Lavalle - A01751912
# Gerardo Gutierrez Paniagua - A01029422

from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agent import ObstacleAgent, BoxAgent, TowerAgent, RobotAgent

class RandomModel(Model):
    """ 
    Se crea un un modelo con agentes
    Args:
        N: Numero de agentes Roomba
        height, width: El tamano del tablero
        density: Probablidad de aparicion de basura en un espacio
        max_time: Tiempo maximo de ejecucion
    """
    def __init__(self, N, num_towers, width, height, density=0.65):
        self.num_agents = N
        self.width = width
        self.height = height
        self.grid = MultiGrid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True
        self.num_towers = num_towers

        # Crea el borde
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        for pos in border:
          obs = ObstacleAgent(pos, self)
          self.grid.place_agent(obs, pos)


        count = 0

        stations = []

        while (count < self.num_towers):
          xt = int(round(self.random.random() * self.width-1))
          yt = int(round(self.random.random() * self.height-1))

          print(xt,yt)
          if self.grid.is_cell_empty((xt,yt)):
            tower = TowerAgent(self, (xt, yt))
            self.grid.place_agent(tower, (xt,yt))
            stations.append((xt,yt))
            count += 1

        count = 0

        while (count < self.num_agents):
          xt = int(round(self.random.random() * self.width-1))
          yt = int(round(self.random.random() * self.height-1))
          if self.grid.is_cell_empty((xt,yt)):
            a = RobotAgent(count,self, stations) 
            self.schedule.add(a)
            self.grid.place_agent(a, (xt,yt))
            count += 1

        count = 0
        # Crear agentes basura en espacios aleatorios
        for (contents, x, y) in self.grid.coord_iter():
          if self.random.random() < density and self.grid.is_cell_empty((x,y)):
            boxAgent = BoxAgent((x,y), self)
            self.grid.place_agent(boxAgent, (x,y))
            count += 1

          if count >= self.num_towers * 5:
            break
            
    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()
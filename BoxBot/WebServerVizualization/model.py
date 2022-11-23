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
    def __init__(self, N, num_towers, width, height):
        self.num_agents = N
        self.width = width
        self.height = height
        self.grid = MultiGrid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True
        self.num_towers = num_towers

        # Crea el borde
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        count = 0

        for pos in border:
          obs = ObstacleAgent(str(count) + "obs", self)
          self.grid.place_agent(obs, pos)
          count += 1


        count = 0

        stations = []

        while (count < self.num_towers):
          xt = int(round(self.random.random() * self.width-1))
          yt = int(round(self.random.random() * self.height-1))

          print(xt,yt)
          if self.grid.is_cell_empty((xt,yt)):
            tower = TowerAgent(str(count)+"tower", (xt, yt))
            self.grid.place_agent(tower, (xt,yt))
            stations.append((xt,yt))
            count += 1

        count = 0

        while (count < self.num_agents):
          xt = int(round(self.random.random() * self.width-1))
          yt = int(round(self.random.random() * self.height-1))
          if self.grid.is_cell_empty((xt,yt)):
            a = RobotAgent(str(count) + "robot",self, stations, (xt, yt)) 
            self.schedule.add(a)
            self.grid.place_agent(a, (xt,yt))
            count += 1

        count = 0
        # Crear agentes basura en espacios aleatorios

        while (count < self.num_towers * 5):
          xt = int(round(self.random.random() * self.width-1))
          yt = int(round(self.random.random() * self.height-1))
          if self.grid.is_cell_empty((xt,yt)):
            a = BoxAgent(str(count)+"box",self) 
            self.schedule.add(a)
            self.grid.place_agent(a, (xt,yt))
            count += 1
            
    def step(self):
      '''Advance the model by one step.'''
      self.schedule.step()
      if self.checkPlaced():
        self.running = False

    def checkPlaced(self):
      """
      Helper method to count trees in a given condition in a given model.
      """
      for box in self.schedule.agents:
          if isinstance(box, BoxAgent):
            if not box.placed:
              return False
      return True
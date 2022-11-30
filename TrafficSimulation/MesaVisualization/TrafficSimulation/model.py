from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agent import *
import json

class Node():
  pos = None
  parent = None
  f = 0
  g = 0
  h = 0
  direction = None
  def __init__(self, pos, direction = None):
     self.pos = pos
     self.direction = direction

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
    """
    def __init__(self, N):

        dataDictionary = json.load(open("mapDictionary.json"))

        self.traffic_lights = []
        self.destinations = []
        self.map = dict()

        with open('2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in ["v", "^", ">", "<"]:
                        agent = Road(f"r_{r*self.width+c}", self, dataDictionary[col])
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.map[(c, self.height - r - 1)] = Node((c, self.height - r - 1), dataDictionary[col])


                    elif col in ["!", "@", "$", "%"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, dataDictionary[col]["direction"], int(dataDictionary[col]["time"]), False if col == "!" or col == "$" else True)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)
                        
                        self.map[(c, self.height - r - 1)] = Node((c, self.height - r - 1), dataDictionary[col]["direction"])

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destinations.append((c, self.height - r - 1))

        self.corners = [(0,0), (0, self.height-1), (self.width-1, 0), (self.width-1, self.height-1)]
        self.N_destinations = len(self.destinations)-1

        # self.map[self.destinations[1]] = Node(self.destinations[1])
        # agent = Car("car2", self, self.destinations[1], self.map)
        # self.grid.place_agent(agent, (23,1))
        # self.schedule.add(agent)

        # self.map[self.destinations[3]] = Node(self.destinations[3])
        # agent = Car("car3", self, self.destinations[3], self.map)
        # self.grid.place_agent(agent, (1,23))
        # self.schedule.add(agent)

        # self.map[self.destinations[4]] = Node(self.destinations[4])
        # agent = Car("car4", self, self.destinations[4], self.map)
        # self.grid.place_agent(agent, (23,23))
        # self.schedule.add(agent)

        # self.map[self.destinations[5]] = Node(self.destinations[5])
        # agent = Car("car5", self, self.destinations[5], self.map)
        # self.grid.place_agent(agent, (6,8))
        # self.schedule.add(agent)

        self.num_agents = N
        self.running = True

    def step(self):
        '''Advance the model by one step.'''

        if self.schedule.steps % 1 == 0:
          for corner in self.corners:
            add = True
            for contents in self.grid.get_cell_list_contents(corner):
              if isinstance(contents, Car):
                print("hihi")
                add = False
            if add: 
              map_copy = self.map.copy()
              random_destination = round(self.random.random()*self.N_destinations)
              map_copy[self.destinations[random_destination]] = Node(self.destinations[random_destination])
              agent = Car(f"{self.schedule.steps}car{corner}", self, self.destinations[random_destination], map_copy)
              self.grid.place_agent(agent, corner)
              self.schedule.add(agent)
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()
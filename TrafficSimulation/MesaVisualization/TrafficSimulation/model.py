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
        
        map = dict()

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
                        map[(c, self.height - r - 1)] = Node((c, self.height - r - 1), dataDictionary[col])


                    elif col in ["!", "@", "$", "%"]:
                        agent = Traffic_Light(f"tl_{r*self.width+c}", self, dataDictionary[col]["direction"], int(dataDictionary[col]["time"]), False if col == "!" or col == "$" else True)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)
                        
                        map[(c, self.height - r - 1)] = Node((c, self.height - r - 1), dataDictionary[col]["direction"])

                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destinations.append((c, self.height - r - 1))

        map[self.destinations[0]] = Node(self.destinations[0])
        agent = Car("car1", self, self.destinations[0], map)
        self.grid.place_agent(agent, (1,1))
        self.schedule.add(agent)

        map[self.destinations[1]] = Node(self.destinations[1])
        agent = Car("car2", self, self.destinations[1], map)
        self.grid.place_agent(agent, (23,1))
        self.schedule.add(agent)

        map[self.destinations[3]] = Node(self.destinations[3])
        agent = Car("car3", self, self.destinations[3], map)
        self.grid.place_agent(agent, (1,23))
        self.schedule.add(agent)

        map[self.destinations[4]] = Node(self.destinations[4])
        agent = Car("car4", self, self.destinations[4], map)
        self.grid.place_agent(agent, (23,23))
        self.schedule.add(agent)

        map[self.destinations[5]] = Node(self.destinations[5])
        agent = Car("car5", self, self.destinations[5], map)
        self.grid.place_agent(agent, (6,8))
        self.schedule.add(agent)

        self.num_agents = N
        self.running = True

    def step(self):
        '''Advance the model by one step.'''
        if self.schedule.steps % 10 == 0:
            for agent in self.traffic_lights:
                agent.state = not agent.state
        self.schedule.step()
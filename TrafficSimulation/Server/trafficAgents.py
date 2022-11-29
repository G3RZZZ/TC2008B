from mesa import Agent

class Node():
  pos = None
  parent = None
  f = 0
  g = 0
  h = 0
  def __init__(self, pos):
     self.pos = pos


class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, destination, city_map):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.model = model
        self.destination = destination
        self.direction = None
        self.timer = 0
        self.previous_pos = None
        self.map = city_map
        self.route  = None

    def calculateRoute(self):
        not_visited= []
        visited = []
        blocked = []

        startNode = self.pos
        finishNode = self.destination

        successors = self.getAheadSpaces(self.map[self.pos].direction, self.pos)
        
        for successor in successors:
          for contents in self.model.grid.get_cell_list_contents(successors):
              if isinstance(contents, Car) or isinstance(contents, Obstacle):
                blocked.append(successor)   
        
        not_visited.append(startNode)

        while len(not_visited) != 0:
          chosenNode = not_visited[0]
          for node in not_visited:
            if self.map[chosenNode].f > self.map[node].f:
              chosenNode = node
          visited.append(chosenNode)
          not_visited.remove(chosenNode)
          
          if not successors:
            successors = self.getAheadSpaces(self.map[chosenNode].direction, self.map[chosenNode].pos)

          for successor in successors:
            add = True
            for open_node in not_visited:
              if open_node == successor:
                add = False
                break;

            for closed_node in visited:
              if closed_node == successor:
                add = False
                break;

            if self.map[successor].pos == self.map[finishNode].pos:
              self.map[finishNode].parent = self.map[chosenNode]
              break;
            
            if add:
              self.map[successor].parent = self.map[chosenNode]

              self.map[successor].g = self.map[chosenNode].g + 1
              self.map[successor].h = self.diagonalDistance(successor, finishNode)
              self.map[successor].f = self.map[successor].g + self.map[successor].h
              not_visited.append(successor)
          successors = None


        calculatedRoute = self.getRoute(self.map[finishNode])
        return calculatedRoute


    def getRoute(self, finish):
        route = []
        current_node = finish
        while not current_node.parent.pos == self.map[self.pos].pos:
          route.append(current_node.pos)
          current_node = current_node.parent
        route.append(current_node.pos)
        route.reverse()

        return route

    def diagonalDistance(self, current, finish):
        dx = abs(current[0] - finish[0])
        dy = abs(current[1] - finish[1])

        D = 1
        D2 = 2**0.5
        
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    
    def checkSensors(self):
        
        steps_ahead = self.getAheadSpaces(self.map[self.pos].direction, self.pos)
        availability = []
        for step in steps_ahead:
          free = True 
          for contents in self.model.grid.get_cell_list_contents(step):
            if isinstance(contents, Car) or isinstance(contents, Obstacle):
              free = False
            if isinstance(contents, Traffic_Light):
              if not contents.state:
                free = False

          availability.append(free)

        next_moves = [x for x, y in zip(steps_ahead, availability) if y]
        return next_moves

    def getAheadSpaces(self, direction, pos):
        surroundings = self.model.grid.get_neighborhood(
          pos,
          moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
          include_center=False)

        possible_steps = []

        sign = 1

        if direction == "Left" or direction == "Down":
          sign = -1

        xAxis = True if direction == "Left" or direction == "Right" else False
        for space in surroundings:
          if space in self.map:
            if xAxis:
              if space[0]*sign >= pos[0]*sign:
                if not ((self.map[space].direction == "Down" and space[1] > pos[1]) or (self.map[space].direction == "Up" and space[1] < pos[1])):
                  possible_steps.append(space)

            else:
              if space[1]*sign >= pos[1]*sign:
                if not ((self.map[space].direction == "Left" and space[0] > pos[0]) or (self.map[space].direction == "Right" and space[0] < pos[0])):
                  possible_steps.append(space)
        
        return possible_steps

    def move(self, steps_ahead):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        route = self.route[0]   
        curr_distance = self.diagonalDistance(self.pos, self.destination)     
        for space in steps_ahead:
            if space == route:
              self.previous_pos = self.pos
              self.model.grid.move_agent(self, space)
              self.route.remove(space)
              return
        
        for space in steps_ahead:
          new_distance = self.diagonalDistance(space, self.destination)
          if new_distance < curr_distance:
            print(new_distance, curr_distance)
            self.previous_pos = self.pos
            self.model.grid.move_agent(self, space)
            self.route = self.calculateRoute()
            return
        


    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        if self.pos == self.destination:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
          steps_ahead = self.checkSensors()
          if self.route == None:
            self.route = self.calculateRoute()
          if self.pos == self.previous_pos:
            self.timer += 1
          if self.timer > 20:
            self.route = self.calculateRoute()
          else:
            self.move(steps_ahead)
            self.timer = 0

class Traffic_Light(Agent):
    """
    Traffic light. Where the traffic lights are in the grid.
    """
    def __init__(self, unique_id, model, direction, timeToChange, state = False):
        super().__init__(unique_id, model)
        """
        Creates a new Traffic light.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            state: Whether the traffic light is green or red
            timeToChange: After how many step should the traffic light change color 
        """
        self.state = state
        self.timeToChange = timeToChange
        self.direction = direction

    def step(self):
        """ 
        To change the state (green or red) of the traffic light in case you consider the time to change of each traffic light.
        """
        # if self.model.schedule.steps % self.timeToChange == 0:
        #     self.state = not self.state
        pass

class Destination(Agent):
    """
    Destination agent. Where each car should go.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Road(Agent):
    """
    Road agent. Determines where the cars can move, and in which direction.
    """
    def __init__(self, unique_id, model, direction= "Left"):
        """
        Creates a new road.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
            direction: Direction where the cars can move
        """
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass



from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
# from agent import *
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

        if self.schedule.steps % 5 == 0:
          for corner in self.corners:
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
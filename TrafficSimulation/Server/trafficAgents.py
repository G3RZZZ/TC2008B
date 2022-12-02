# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
'''
Gerardo Gutiérrez Paniagua, A01029422
Mateo Herrera Lavalle A01751912
Francisco Daniel Salcedo Catalán A01633010
Regina Rodríguez Sánchez A01284329
'''
# Novimebre 2022
# Octavio Navarro. October 2021

# This script contains both the agent and model classes that define the simulation


from mesa import Agent

# Class that conforms the car agent in the simultation
class Car(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: The agent's unique ID
        model: Variable that contains the model
        destination: Variable that contains the x, y coordinates of the destination
        direction: Variable that holds the current direction
        timer: Variable that repesents how many steps the agent has stayed in place
        previous_pos: Variable that contains the agent's previous position
        map: Variabe that contains a dictionary that represents the map
        route: Variable that holds a list that represents a route to a destination
        deviate: Boolean variable that is tue once enough time passes. This variable,
        controls whether or not a car should stay on course or not.
        arrived: Boolean variable that is true when vehicle arrives at destination
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
        self.deviate = False
        self.arrived = False

    # Function that uses a modified version of the A* algorithm to chart a route
    # froom the current position to the destination
    def calculateRoute(self):
        # Initialize variables
        not_visited= []
        visited = []
        startNode = self.pos
        finishNode = self.destination
        
        # Append first node to not visited list
        not_visited.append(startNode)

        # Iterate through not visited list while it is not empty
        while len(not_visited) != 0:

          # Initialize chosen node as the first value in not_visited list
          chosenNode = not_visited[0]

          # Select node with lowest f
          for node in not_visited:
            if self.map[chosenNode].f > self.map[node].f:
              chosenNode = node
          
          # append to visited list and remove from not visiited
          visited.append(chosenNode)
          not_visited.remove(chosenNode)
          
          # Get node successors while taking into account current direction
          successors = self.getAheadSpaces(self.map[chosenNode].direction, self.map[chosenNode].pos)
          
          # Iterate through node succesors
          for successor in successors:

            # If node is either already in the open or closed list ignore it
            add = True
            for open_node in not_visited:
              if open_node == successor:
                add = False
                break;

            for closed_node in visited:
              if closed_node == successor:
                add = False
                break;
            
            # Check if succesor node is finish node, if not, continue
            if self.map[successor].pos == self.map[finishNode].pos:
              self.map[finishNode].parent = self.map[chosenNode]
              break;
            
            # Calculate g, h and f values and assign parent node
            if add:
              self.map[successor].parent = self.map[chosenNode]

              self.map[successor].g = self.map[chosenNode].g + 1
              self.map[successor].h = self.diagonalDistance(successor, finishNode)
              self.map[successor].f = self.map[successor].g + self.map[successor].h
              # Append node to not_visited
              not_visited.append(successor)
          successors = None

        # Get route recursively
        calculatedRoute = self.getRoute(self.map[finishNode])
        return calculatedRoute


    # Auxiliary function that fetches the route fom position to finish recursively
    def getRoute(self, finish):
        # Initialize variables
        route = []
        current_node = finish
        
        # Iterate through node parents until parent equals current position
        while not current_node.parent.pos == self.map[self.pos].pos:
          route.append(current_node.pos)
          current_node = current_node.parent
        route.append(current_node.pos)
        
        # Reverse route at end
        route.reverse()

        # Return calculated route if it is not empty
        if len(route) > 0:
          return route
        else:
          return self.route

    # Auxiliary function that calculates de heuristic diaginal distance to a node
    def diagonalDistance(self, current, finish):
        dx = abs(current[0] - finish[0])
        dy = abs(current[1] - finish[1])

        D = 1
        D2 = 2**0.5
        
        return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    
    # Function that checks neighboring spaces and returns available ones
    def checkSensors(self):
        # Get steps that are ahead relative to cars direction
        steps_ahead = self.getAheadSpaces(self.map[self.pos].direction, self.pos)
        
        # Get rearview mirros positions (Positions that are to the sides)
        xAxis = True if self.map[self.pos].direction == "Left" or self.map[self.pos].direction == "Right" else False
        x, y = self.pos
        side1 = (x, y + 1) if xAxis else (x + 1, y)
        side2 = (x, y - 1) if xAxis else (x - 1, y)

        availability = []

        # Iterate through steps ahead and check if they are a possible move space
        for step in steps_ahead:
          free = True 
          # Check if space has a car or is a red light
          for contents in self.model.grid.get_cell_list_contents(step):
            if isinstance(contents, Car) or isinstance(contents, Obstacle):
              free = False
            if isinstance(contents, Traffic_Light):
              if not contents.state:
                free = False

            # Check rear view mirroes and determine if turning is possible
            if xAxis:
              if step[1] == y + 1:
                for side in self.model.grid.get_cell_list_contents(side1):
                  if isinstance(side, Car):
                    free = False
              elif step[1] == y - 1:
                for side in self.model.grid.get_cell_list_contents(side2):
                  if isinstance(side, Car):
                    free = False
            else:
              if step[0] == x + 1:
                for side in self.model.grid.get_cell_list_contents(side1):
                  if isinstance(side, Car):
                    free = False
              elif step[0] == x - 1:
                for side in self.model.grid.get_cell_list_contents(side2):
                  if isinstance(side, Car):
                    free = False

          availability.append(free)

        # Get possible next moves if available
        next_moves = [x for x, y in zip(steps_ahead, availability) if y]
        return next_moves

    # Auxiliary function that returns front positions relative to direction
    def getAheadSpaces(self, direction, pos):
        surroundings = self.model.grid.get_neighborhood(
          pos,
          moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
          include_center=False)

        possible_steps = []

        # Initialize variable
        sign = 1

        # Change sign if direction is left or down
        if direction == "Left" or direction == "Down":
          sign = -1

        # Cheeck movement axis
        xAxis = True if direction == "Left" or direction == "Right" else False
        
        # Iterate through spaces in surroundings
        for space in surroundings:

          # Check if previous position is the same as space where you'll move to
          if space in self.map and space != self.previous_pos:

            # Evaluate if space is in fron relative to direction
            if xAxis:
              if space[0]*sign > pos[0]*sign:
                if not ((self.map[space].direction == "Down" and space[1] > pos[1]) or (self.map[space].direction == "Up" and space[1] < pos[1])):
                  possible_steps.append(space)

            else:
              if space[1]*sign > pos[1]*sign:
                if not ((self.map[space].direction == "Left" and space[0] > pos[0]) or (self.map[space].direction == "Right" and space[0] < pos[0])):
                  possible_steps.append(space)
        
        # Return possible steps
        return possible_steps

    # Auxiliary function that checks distance to route
    def check_deviation(self, space, route_space):
      xd = abs(space[0] - route_space[0])
      yd = abs(space[1] - route_space[1])

      if xd > 1 or yd > 1:
        return False
      return True

    # Function that moves car agent
    def move(self, steps_ahead):
        """ 
        Determines if the agent can move in the direction that was chosen
        """

        # Get route next pos
        next_route = self.route[0]
        # Get current route
        route = self.route   

        # Iterate thorugh available spaces and move to route if possible
        for space in steps_ahead:
            if space in self.route:
              self.deviate = False
              self.model.grid.move_agent(self, space)
              self.route = route[route.index(space)+1:]
              return

        # If not evaluate if enough time has been waited to change lanes
        if self.timer > 2:
          self.deviate = True

        # If enough time has passed move to new position
        move_space = None
        low_distance = float("inf")
        for space in steps_ahead:
          curr_distance = self.diagonalDistance(space, self.destination)
          if curr_distance < low_distance:
            if self.check_deviation(space, next_route):
              move_space = space;
              break;
            else:
              move_space = space;
          
        if move_space and self.deviate:
          if len(self.route) > 3:
            self.model.grid.move_agent(self, move_space)
            self.route.remove(next_route)
            return
          else:
            self.model.grid.move_agent(self, move_space)
          
        # if self.deviate and len(steps_ahead) > 0:
        #   self.route = self.calculateRoute()
        

    # Function that determines what the car will do
    def step(self):

        # If positio is equal to destination, delete car in next step and change
        # arrived to true
        # (Unity needs a signal to delete game object)
        self.previous_pos = self.pos
        if self.pos == self.destination:
            if self.arrived:
              self.model.grid.remove_agent(self)
              self.model.schedule.remove(self)
            self.arrived = True
        else:
          # Move when possible and recalculate route if enoughtime has passed
          steps_ahead = self.checkSensors()
          if self.route == None:
            self.route = self.calculateRoute()
          elif self.timer > 20 and len(steps_ahead) > 0:
            self.route = self.calculateRoute()
            self.timer = 0
          else:
            self.move(steps_ahead)
          
          # Increase  timer if previous position is equal to current position
          if self.pos == self.previous_pos:
            self.timer += 1
          else:
            self.timer = 0

# Class that represents a traffic light agent
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
            direction: direction
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
import json

# Class used for map dictionary creation 
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


# Class that represents model
class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        traffic_lights: List that contains traffic ligt
        destinations: List that contains destination
        map: Dictionary of map
        N: Number of agents in the simulation
    """
    def __init__(self, N):

        # Load data from txt file
        dataDictionary = json.load(open("mapDictionary.json"))

        # Initialize variables
        self.traffic_lights = []
        self.destinations = []
        self.map = dict()

        # Read simbols and place agents on correct positions
        with open('2022_base.txt') as baseFile:
            lines = baseFile.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)

            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            # Place siimbols in correct positions and add roads an traffic lights
            # to dictionary with node class
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

        # Get corners where cars will spawn as well as the number of destinations
        self.corners = [(0,0), (0, self.height-1), (self.width-1, 0), (self.width-1, self.height-1)]
        self.N_destinations = len(self.destinations)-1

        # Start model
        self.num_agents = N
        self.running = True

    def step(self):
        '''Advance the model by one step.'''

        if self.schedule.steps % 1 == 0:
          # Add car in corner each n steps if space is free
          for corner in self.corners:
            add = True
            for contents in self.grid.get_cell_list_contents(corner):
              if isinstance(contents, Car):
                add = False
            if add: 
              # Add random direction  to map of instab=ntiated agent
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
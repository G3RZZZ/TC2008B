from mesa import Agent

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0
        self.id = unique_id

    def check_neighbor_trash(self, neighborPos):
      typeList = self.model.grid.get_cell_list_contents(neighborPos)
      sameAgentCount = 0
      pos = ()
      for type in typeList:
        if isinstance(type, TrashAgent):
          pos =  neighborPos
        elif isinstance(type, RandomAgent):
          sameAgentCount = 1
      return (pos, sameAgentCount)
        
      
    def clean(self):
      typeList = self.model.grid.get_cell_list_contents(self.pos)
      for type in typeList:
        if isinstance(type, TrashAgent):
          self.model.grid.remove_agent(type)

    def move(self, posList):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        next_move = self.random.choice(posList)
        self.model.grid.move_agent(self, next_move)
        self.steps_taken+=1

    def checkSensors(self):
      possible_steps = self.model.grid.get_neighborhood(
        self.pos,
        moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
        include_center=True)
      trashSpaces = []
      nextMoves = []
      for coords in possible_steps:
        trashpos, sameCount = self.check_neighbor_trash(coords)
        if trashpos:
          if coords == self.pos:
            return
          trashSpaces.append(coords)
        elif self.model.grid.is_cell_empty(coords):
          nextMoves.append(coords)

      if trashSpaces and self.id > sameCount:
        return trashSpaces
      elif nextMoves and self.id > sameCount:
        return nextMoves
      else:
        return [self.pos]



    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        # self.direction = self.random.randint(0,8)
        # print(f"Agente: {self.unique_id} movimiento {self.direction}")
        sensorInfo = self.checkSensors()
        if not sensorInfo:
          self.clean()
        else:
          self.move(sensorInfo)

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

class TrashAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass    

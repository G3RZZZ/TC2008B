# -*- coding: utf-8 -*-
"""
Modelos de Agente y del medio ambiente
Movimiento aleatorio del auto en el grid

Solución al reto de TC2008B semestre AgostoDiciembre 2021
Autor: Jorge Ramírez Uresti, Octavio Navarro
"""

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

class RobotAgent(Agent):
    """
    Agente que se mueve aleatoriamente y limpia basura al encontrarla.
    Attributes:
        unique_id: Id del agente
        direction: Direccion que elige el agente
        steps_taken: Cuantos pasos a dado el agente
    """

    def __init__(self, unique_id, model, stations, pos):
        """
        Inicializa el agente
        Args:
            unique_id: The agent's ID
            model: Modelo del agente
        """
        super().__init__(unique_id, model)
        self.steps_taken = 0
        self.unique_id = unique_id
        self.previous_pos = []
        self.stations = stations
        self.carry_box = None
        self.look_here = pos
    


    # def get_neighbor_type(self, neighborPos):
    #   """
    #   Funcion que regresa la posicion de un agente cuando este es basura,  y
    #   tambien regresa el numero de agentes de Roomba hay en los espacios
    #   """
    #   typeList = self.model.grid.get_cell_list_contents(neighborPos)
    #   box = False
    #   free_space = True
    #   if not self.model.grid.is_cell_empty(neighborPos):
    #     free_space = False
    #     for type in typeList:
    #       if isinstance(type, BoxAgent):
    #         box =  True
    #   return (free_space, box)

    def checkSensors(self):
      """ 
      Funcion que analiza los espacios scercanos al agente del Roomba y regresa
      una lista de espacios a los que moverse. En caso de encontrar basura en el
      espacio actual no regresa nada.
      """
      possible_steps = self.model.grid.get_neighborhood(self.pos, moore = False)

      next_moves = []
      for coords in possible_steps:
        neighbor_contents =  self.model.grid.get_cell_list_contents(coords)
        if neighbor_contents:
          for neighbor in neighbor_contents:
            if isinstance(neighbor, BoxAgent) and not self.carry_box and len(neighbor_contents) == 1:
              return (coords, True)
            elif isinstance(neighbor, TowerAgent) and self.carry_box and coords in self.stations: 
              return (coords, True)
        else:
          next_moves.append(coords)

      if next_moves:
        return (next_moves, False)
      return ([self.pos], False)

    def explore(self, posList):
      """ 
      Moverse a un espacio aleatorio de la lista de espaacios proporcionada.
      """
      next_move = self.random.choice(posList)
      self.model.grid.move_agent(self, next_move)
      self.steps_taken+=1
      self.look_here = self.pos

    def pickUp(self, boxPos):
      print(1)
      typeList = self.model.grid.get_cell_list_contents(boxPos)
      for agent in typeList:
        if isinstance(agent, BoxAgent):
          self.model.grid.move_agent(agent, self.pos)
          self.carry_box = agent
      self.look_here = boxPos

    def returnToTower(self,  posList):
      xs, ys = self.pos
      stations = self.stations
      stations.sort(key = lambda pos: (pos[0] - xs) ** 2 + (pos[1] - ys) ** 2)
      station = stations[0]
      x_stat, y_stat = station
      posList.sort(key = lambda pos: (pos[0] - x_stat) ** 2 + (pos[1] - y_stat) ** 2)

      for pos in posList:
        if pos not in self.previous_pos:
          self.previous_pos.append(self.pos)
          self.model.grid.move_agent(self, pos)
          self.model.grid.move_agent(self.carry_box, pos)
          self.look_here = self.pos
          return
      
      if self.previous_pos:
        pos = self.previous_pos.pop()
        self.previous_pos.insert(0, self.pos)
        self.model.grid.move_agent(self, pos)
        self.model.grid.move_agent(self.carry_box, pos)

      self.look_here = self.pos


    def place(self, coords):
      self.previous_pos.clear()
      contents = self.model.grid.get_cell_list_contents(coords)
      if not len(contents) >= 6:
        self.model.grid.move_agent(self.carry_box, coords)
        self.carry_box.placed = True
        self.carry_box = False
      else: 
        self.stations.remove(coords)

      self.look_here = coords

    def step(self):
        """ 
        Dependiendo de lo que regresen los sensorees, se mueve el robot o se 
        limpia el espacio.
        """
        # self.direction = self.random.randint(0,8)
        # print(f"Agente: {self.unique_id} movimiento {self.direction}")
        coords, box = self.checkSensors()
        if self.carry_box and box:
          self.place(coords)
          return
        elif self.carry_box:
          self.returnToTower(coords)
          return

        if box:
          self.pickUp(coords)
        else:
          self.explore(coords)

class ObstacleAgent(Agent):
    """
    Agente que representa un obstaculo
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

class BoxAgent(Agent):
    """
    Agente que representa un espacio basura
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.placed = False

    def step(self):
        pass    


class TowerAgent(Agent):
    """
    Agente que representa un espacio basura
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass    

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
from random import choice
import pygame
import Directions as direction
import NeuralNet as nn
from enum import Enum

class MoveType(Enum):
    USER = 0
    SELF = 1
    NN = 2

class Bug(pygame.sprite.Sprite):

    def __init__(self, x, y, map_size) -> None:
        super().__init__()
        self.map_size = map_size
        self.position = pygame.Vector2(x, y)
        self.surf = pygame.Surface((1,1))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center = self.position)
        self.nn = nn.NeuralNet()
        self.move_strategy = self.move_directed
        self.sight_neurons = {key: self.nn.get_input() for key in direction.map.keys()} 
        self.movement_neurons = {key: self.nn.get_output() for key in direction.map.keys()}
        self.nn.connectIO()
        self.move_type = self.chase_light
        self.light_vals = {}

    def set_move_strat(self, type):
        if type == MoveType.USER:
            self.move_strategy = self.move_directed
        elif type == MoveType.NN:
            self.move_strategy = self.learn_move
        else:
            self.move_strategy = self.chase_light

    def get_location(self):
        return self.position

    #Basic functions
    def eat(self, food_val):
        self.nn.reward(food_val)

    def move(self, event = None):
        dir, is_learn_move = self.move_strategy(event)
        new_x = self.position.x + dir[0]
        new_y = self.position.y + dir[1]
        if(new_x <= 0 or new_x >= self.map_size[0] or new_y <= 0 or new_y >= self.map_size[1]):
            dir = direction.NONE
        self.position += dir
        self.rect.center = self.position
        return is_learn_move

    #Movement strategies
    def move_directed(self, event = None):
        if event != None:
            if event.key == pygame.K_UP:
                return direction.UP, False
            elif event.key == pygame.K_DOWN:
                return direction.DOWN, False
            elif event.key == pygame.K_LEFT:
                return direction.LEFT, False
            elif event.key == pygame.K_RIGHT:
                return direction.RIGHT, False
        else:
            return direction.NONE, False

    def chase_light(self, event = None):
        max_key = max(self.light_vals, key=self.light_vals.get)
        result = list(filter(lambda x:x[1] == self.light_vals[max_key],self.light_vals.items()))

        #Right now this can get stuck on the borders, since the lights are
        #drawn outside the boundaries of the graph
        if (len(result) == 1):
            return direction.map[max_key], False
        else:
            return direction.map[choice(result)[0]], False #choose randomly from equal values

    def learn_move(self, event = None):
        sees_light = False
        for k, v in self.light_vals.items():
            self.sight_neurons[k].activate(v)
            if v > 0:
                sees_light = True
        self.nn.cascade()
        max_weight = 0
        dir = None

        #TODO Thematically, this should be "listening" to the motor neurons
        for k, v in self.movement_neurons.items():
            if v.act_potential > max_weight:
                max_weight = v.act_potential
                dir = k
        if sees_light:
            return direction.map[dir] if not dir == None else direction.NONE, True # If it sees the light, only move on purpose.
        else:
            return choice(list(direction.map.values())), False
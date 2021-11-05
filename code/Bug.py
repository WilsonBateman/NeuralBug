from random import choice
import pygame
import Coordinates as cd
import operator
import NeuralNet as nn
from enum import Enum

FOODMAX = 255

class MoveType(Enum):
    USER = 0
    SELF = 1
    NN = 2

class Bug(pygame.sprite.Sprite):

    def __init__(self, x, y) -> None:
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.surf = pygame.Surface((1,1))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center = self.position)
        self.nn = nn.NeuralNet()
        self.move_strategy = self.move_directed
        self.sight_neurons = {key: self.nn.get_input() for key in cd.coords.keys()} 
        self.movement_neurons = {key: self.nn.get_output() for key in cd.coords.keys()}
        self.nn.connectIO()
        self.move_type = self.chase_light
        self.light_vals = {}

    def set_move_strat(self, type):
        if type == MoveType.USER:
            self.move_strategy = self.move_directed
        elif type == MoveType:
            self.move_strategy = self.learn_move
        else:
            self.move_strategy = self.chase_light

    def get_location(self):
        return self.position

    #Basic functions
    def eat(self, food_val):
        print("Food: {}".format(food_val))
        self.nn.reward(food_val/FOODMAX)

    def move(self, event = None): #Need to constrain to map
        dir = self.move_strategy(event)
        self.position += dir
        self.rect.center = self.position

    def look_direction(self, d):
        try:
            return self.look(tuple(map(operator.add, self.position, d)))
        except:
            print("Eyes not set correctly or looking out of bounds.")

    #Movement strategies
    def move_directed(self, event = None):
        if event != None:
            if event.key == pygame.K_UP:
                return cd.coords["up"]
            elif event.key == pygame.K_DOWN:
                return cd.coords["down"]
            elif event.key == pygame.K_LEFT:
                return cd.coords["left"]
            elif event.key == pygame.K_RIGHT:
                return cd.coords["right"]
        else:
            return pygame.Vector2(0,0)

    def chase_light(self, event = None):
        max_key = max(self.light_vals, key=self.light_vals.get)
        result = list(filter(lambda x:x[1] == self.light_vals[max_key],self.light_vals.items()))

        #Right now this can get stuck on the borders, since the lights are
        #drawn outside the boundaries of the graph
        if (len(result) == 1):
            return cd.coords[max_key]
        else:
            return cd.coords[choice(result)[0]] #choose randomly from equal values

    def learn_move(self, event = None):
        for k, v in self.sight_neurons.items():
            v.activate(self.look_direction(cd.coords[k]))
        self.nn.cascade()
        max_weight = 0
        dir = pygame.Vector2(0, 0)

        for k, v in self.movement_neurons.items():
            if v.act_potential > max_weight:
                max_weight = v.act_potential
                dir = k
        return dir # move in the direction of the most action potential
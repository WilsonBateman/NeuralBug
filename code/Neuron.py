from numpy import False_
from pygame.constants import ACTIVEEVENT
from Dendrite import Dendrite
import math

#First the neuron will determine whether to fire (given input and depletion)
#That will give its action potential. From there, it will determine which 
#connected neurons to activate and which to inhibit.
#Reward will be weighted depending on level of depletion.
class Neuron:

    def __init__(self):
        self.act_potential = 0.0
        self.connections = {}
      
    #Add and give activation weights
    def add_connections(self, connections = {}):
        self.connections = {Dendrite(neuron, .1) for neuron in connections}

    def reinitialize(self):
        self.act_potential = 0
        for connection in self.connections:
            connection.reinitialize()

    def activate(self, new_act):
        self.act_potential += new_act
        if (self.act_potential > 1):
            self.act_potential = 1

    def propogate(self):
        for connection in self.connections:
            connection.activate(self.act_potential)

    def reward(self, reward_ratio):
         for d in self.connections:
            d.reward(reward_ratio)

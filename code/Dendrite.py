from random import random
import globals

class Dendrite:

    def __init__(self, neuron, weight: float) -> None:
        self.neuron = neuron #Downstream neuron
        self.weight = weight
        self.fired = False

    def reinitialize(self):
        self.fired = False

    def activate(self, action_potential):
        if (action_potential > 0 and random() < self.weight):
            self.neuron.activate(action_potential) #Or strength?
            self.fired = True

    def reward(self, reward_ratio):
        if (self.fired):
            if (reward_ratio > 0): #Just to save the calcs
                #print("REWARD!")
                self.weight += globals.reward #Most are going to be misses, so this needs to weight more heavily
            elif (reward_ratio == 0): #Failure hits hard, always has a 1% chance to fire
                self.weight -= globals.punishment
        else:
            self.weight -= globals.falloff

        if self.weight < 0.01:
            self.weight = 0.01
        elif self.weight > .99:
            self.weight = .99
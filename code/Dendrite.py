from random import random

fall_off = .05 #Want something that would take a few rounds to fade away

class Dendrite:

    def __init__(self, neuron, weight: float) -> None:
        self.neuron = neuron #Downstream neuron
        self.weight = weight
        self.strength = 0.0
        self.fired = False

    def activate(self, action_potential):
        self.strength = action_potential * self.weight #Get the chance to fire.
        if (random() < self.strength):
            self.neuron.activate(self.strength)
            self.fired = True

    def reward(self, reward_ratio):
        if (self.fired and reward_ratio > 0): #Just to save the calcs
            print("REWARD!")
            self.weight += .05 #Most are going to be misses, so this needs to weight more heavily
        elif (self.weight > .05):
            self.weight -= .0001

        self.strength = 0.0
        self.fired = False
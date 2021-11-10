from random import random

class Dendrite:

    def __init__(self, neuron, weight: float) -> None:
        self.neuron = neuron #Downstream neuron
        self.weight = weight
        self.fired = False

    def activate(self, action_potential):
        if (random() < self.weight):
            self.neuron.activate(action_potential) #Or strength?
            self.fired = True

    def reward(self, reward_ratio):
        if (self.fired):
            if (reward_ratio > 0 and self.weight < .99): #Just to save the calcs
                #print("REWARD!")
                self.weight += .01 #Most are going to be misses, so this needs to weight more heavily
            elif (reward_ratio == 0 and self.weight > .01): #Failure hits hard
                self.weight -= .0003
        # elif (self.weight > .01):
        #     self.weight -= .000001

        self.fired = False
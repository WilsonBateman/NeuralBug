from random import random

class Dendrite:

    def __init__(self, neuron, weight: float) -> None:
        self.neuron = neuron
        self.weight = weight
        self.depletion = 0.0 #might end up a bool

    def activate(self, action_potential):
        signal_strength = action_potential * self.weight * (1 - self.depletion) * random()
        self.depletion += signal_strength
        self.neuron.activate(signal_strength)

    def reward(self, reward_ratio):
        reward = reward_ratio * self.depletion
        self.depletion = 0.0
        if self.weight > 0:
            self.weight += reward
        else:
            self.weight -= reward
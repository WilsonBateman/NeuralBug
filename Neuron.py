from random import random

fall_off = .5 #Want something that would take a few rounds to fade away
threshhold = .5
variance = 2

class Neuron:

    def __init__(self, connections = {}) -> None:
        self.connections = connections
        self.act_potential = 0

    #Add and give activation and inhibition weights
    def add_connections(self, connections = {}):
        self.connections = {key: (.5, .5) for key in connections}

    def activate(self, weight):
        self.act_potential += weight
    
    def inhibit(self, weight): #This won't play in until at least two rows of neurons
        self.act_potential += weight

    def propogate(self):
        lambda x: self.choose_fire(x, self.act_potential) in self.connections

    def choose_fire(self, connection, weight):
        activatrix = random.uniform(0,variance)
        if activatrix * connection[1] > threshhold:
            print("weight = {}, falloff = {}".format(activatrix * connection[1], fall_off))
            connection[0].activate(weight* fall_off)

    def reward(self, reward_ratio):
         for k, (a, i) in self.connections.items():
            a *= ((reward_ratio+1)) #No reward if not fired
            k.reward(reward_ratio) #This rewards all "listeners instead of the firing neuron"


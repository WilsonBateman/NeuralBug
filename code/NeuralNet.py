from random import choice
from Neuron import Neuron

gen_len = 50
max_row_size = 4
max_columns = 2

def add_neuron(n_type):
    neuron = Neuron()
    n_type.append(neuron)
    return neuron

class NeuralNet:

    def __init__(self) -> None:
        self.inputs = []
        self.outputs = []
        self.net = [[Neuron() for x in range(max_row_size)] for y in range(max_columns)]

    #Each row will propogate sequentially, allowing synchronicity of inhibitors
    def cascade(self):
        for row in self.net:
            for neuron in row: 
                neuron.propogate()
        print(self.net)

    def get_input(self): #Need to accept a strategy here long-term
        return add_neuron(self.inputs)

    def get_output(self): #Need to accept a strategy here long-term
        return add_neuron(self.outputs)

    def connectIO(self):
        for n in self.inputs : n.add_connections(self.net[0])
        for n in range(len(self.net)-1): #For all but the last row, which will go to outputs
            for m in range(len(self.net[n])):
                self.net[n][m].add_connections(self.net[n+1])
        for n in self.net[len(self.net)-1] : n.add_connections(self.outputs)

    def reward(self, reward_ratio):
        #Use feedback or propogate some sort of confirmation through all cells?
        for n in self.net:
            for m in n:
                m.reward(reward_ratio)
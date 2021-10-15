from random import choice
from Neuron import Neuron

rows = 5
columns = 5
inputs = []
outputs = []
net = [[Neuron() for x in range(rows)] for y in range(columns)]

def get_input(): #Need to accept a strategy here long-term
    return add_neuron(inputs)

def get_output(): #Need to accept a strategy here long-term
    return add_neuron(outputs)

def add_neuron(list_to_use):
    neuron = Neuron()
    list_to_use.append(neuron)
    return neuron

def connectIO():
    for n in inputs : n.add_connections(net[0])
    for n in range(rows-1): #for all but the last row, which will go to outputs
        for m in range(columns):
            net[n][m].add_connections(net[n+1])
    for n in net[rows-1] : n.add_connections(outputs)

def reward(reward_ratio):
    #Use feedback or propogate some sort of confirmation through all cells?
    for n in net:
        for m in n:
            m.reward(reward_ratio)
from Dendrite import Dendrite

#First the neuron will determine whether to fire (given input and depletion)
#That will give its action potential. From there, it will determine which 
#connected neurons to activate and which to inhibit.
#Reward will be weighted depending on level of depletion.
class Neuron:

    act_potential = 0.0
      
    #Add and give activation/inhibition weights
    def add_connections(self, connections = {}):
        self.connections = {Dendrite(neuron, .5) for neuron in connections}     #activations
        #self.connections = {neuron: Dendrite(neuron, -.5) for neuron in connections}    #inhbitions

    def activate(self, weight): #Activate or inhibit
        self.act_potential += weight

    def propogate(self):
        for connection in self.connections:
            connection.activate(self.act_potential)
        self.act_potential = 0

    def reward(self, reward_ratio):
         for d in self.connections:
            d.reward(reward_ratio)

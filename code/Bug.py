from random import choice
import Coordinates as cd
import operator
import NeuralNet as nn

food_max = 255

class Bug:

    def __init__(self, x, y, bound_x, bound_y) -> None:
        self.position = ([x, y])
        self.bound_x = bound_x
        self.bound_y = bound_y
        self.nn = nn.NeuralNet()
        self.sight_neurons = {key: self.nn.get_input() for key in cd.coords.keys()} 
        self.movement_neruons = {key: self.nn.get_output() for key in cd.coords.keys()}
        self.nn.connectIO()

    def get_location(self):
        return self.position

    #Basic functions
    def eat(self, food_val):
        print("Food: {}".format(food_val))
        self.nn.reward(food_val/food_max)

    def give_sight(self, sight_func):
        self.look = sight_func

    def move(self, direction):
        new_x = self.position[0] + direction[0]
        new_y = self.position[1] + direction[1]
        if (new_x > 0 and new_x < self.bound_x):
            self.position[0] = new_x
        if (new_y > 0 and new_y < self.bound_y):
            self.position[1] = new_y

    def look_direction(self, d):
        try:
            return self.look(tuple(map(operator.add, self.position, d)))
        except:
            print("Eyes not set correctly or looking out of bounds.")

    #Movement strategies
    def move_directed(self, event = None):
        if event != None:
            self.move(cd.coords[event.key])

    def chase_light(self, event = None):
        pixel_vals = {key: self.look_direction(cd.coords[key]) for key in cd.coords.keys()}

        max_key = max(pixel_vals, key=pixel_vals.get)
        result = list(filter(lambda x:x[1] == pixel_vals[max_key],pixel_vals.items()))

        #Right now this can get stuck on the borders, since the lights are
        #drawn outside the boundaries of the graph
        if (len(result) == 1):
            self.move(cd.coords[max_key])
        else:
            self.move(cd.coords[choice(result)[0]]) #choose randomly from equal values

    def learn_move(self, event = None):
        pixel_vals = {key: self.look_direction(cd.coords[key]) for key in cd.coords.keys()}
        for k, v in self.sight_neurons.items():
            v.activate(pixel_vals[k])
        self.nn.cascade()
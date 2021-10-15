from random import randint, random
from PIL import Image

class FeedImage:
    width = 200
    height = 200
    
    def initialize(self):
        for x in range(0, self.width-1):
            for y in range(0, self.height-1):
                self.pixels[x, y] = 0

    def addLight(self, x, y):
        color = 5 #start at black
        fade = 5
        step = 256 // fade
        while color <= 256:
            for x_pixel in range (x-step, x+step): #could stand some speeding up
                for y_pixel in range (y-step, y+step):
                    if x_pixel > -1 and x_pixel < self.image.width and y_pixel > -1 and y_pixel < self.image.height:
                        self.pixels[x_pixel,y_pixel] = color
            color += fade # increase the brightness
            step -= 1 # move one more step away from the main pixel
    
    def addLights(self, list_o_lights = [(randint(0, width-1),randint(0, height-1))]):
        self.initialize()
        for light in list_o_lights:
            self.addLight(light[0], light[1])

    def createNew(self):
        self.image = Image.new(mode="L", size = (self.width, self.height), color = 0)
        self.pixels = self.image.load()
        self.initialize()

    def draw_pixel(self, position):
        self.pixels[position[0], position[1]] = 255

    def clear_space(self, position):
        self.pixels[position[0], position[1]] = 0

    def get_pixel(self, position):
        light_val = self.pixels[position[0], position[1]]
        return light_val

    def __init__(self, width, height) -> None:
        width = width
        height = height
        self.height = height
        self.width = width
        self.createNew()
        self.addLights()
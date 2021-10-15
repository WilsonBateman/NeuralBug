from random import randint, random
from PIL import Image

class FeedImage:
    def addLight(self, x, y):
        pixels = self.image.load()
        color = 5 #start at black
        fade = 5
        step = 256 // fade
        while color <= 256:
            for x_pixel in range (x-step, x+step):
                for y_pixel in range (y-step, y+step):
                    if x_pixel > -1 and x_pixel < self.image.width and y_pixel > -1 and y_pixel < self.image.height:
                        pixels[x_pixel,y_pixel] = (color)
            color += fade # increase the brightness
            step -= 1 # move one more step away from the main pixel
    
    def addLights(self, amt = 1):
        for light in range(0, 1):
            self.addLight(randint(0, self.width), randint(0, self.height))

    def createNew(self):
        self.image = Image.new(mode="L", size = (self.width, self.height), color = 0)

    def draw_bug(self, position):
        pixels = self.image.load()
        pixels[position[0], position[1]] = 255
        self.image.show()

    def clear_bug(self, position):
        pixels = self.image.load()
        pixels[position[0], position[1]] = 0

    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.createNew()
        self.addLights()
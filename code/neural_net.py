import pygame
from pygame.locals import *
import sys
from Bug import Bug, MoveType
import math
import Directions as directions
import random
from InputBox import InputBox
import numpy
import globals

FOOD_MAX = 255
SWARM_SIZE = 20 #best if even
MAP_SIZE = (600, 400)
HUD_HEIGHT = 100
LIGHTS_DELAY = 10
NUM_LIGHTS = 500

#Blue to red from 0 to 1
def get_color_map(value):
    return (255 * value, 0, 255 * (1-value))

def draw_neurons(surface, nn, is_reward):
    col_center = 10
    conn_starts = {}
    conn_starts = print_column_at(surface, nn.inputs, col_center, conn_starts, is_reward)
    col_center += 30
    for row in nn.net:
        conn_starts = print_column_at(surface, row, col_center, conn_starts, is_reward)
        col_center += 30
    conn_starts = print_column_at(surface, nn.outputs, col_center, conn_starts, is_reward)


def print_column_at(surface, col, col_center, conns, is_reward):
    new_conns = {}
    next_box = 0
    for n in col:
        next_box +=  20
        if not is_reward:
            #Draw neuron squares
            pygame.draw.rect(surface, get_color_map(n.act_potential), (col_center, next_box, 10, 10))
        #Draw connection lines
        for (start, neuron), (weight, fired) in conns.items():
            if (n == neuron):
                if (is_reward):
                    if(fired):
                        pygame.draw.line(surface, (255,255,0,255), (start[0]+5,start[1]+5), (col_center+5, next_box+5))
                else:
                    pygame.draw.line(surface, get_color_map(weight), (start[0]+5,start[1]+5), (col_center+5, next_box+5), 2)
        #Get the latest neuron's connections
        new_conns.update({((col_center, next_box),d.neuron): (d.weight, d.fired) for d in n.connections})
    return new_conns

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = MAP_SIZE
        self.bug = Bug(100, 100, MAP_SIZE)
        self.lightSprites  = pygame.sprite.Group()
        self.timer = 0
 
    def on_init(self):
        pygame.init()
        self.hud_surf = pygame.Surface((MAP_SIZE[0], HUD_HEIGHT))
        self.text_surf = pygame.Surface((MAP_SIZE[0]//2, HUD_HEIGHT))
        self.reward_overlay = pygame.Surface((MAP_SIZE[0]//2, HUD_HEIGHT), pygame.SRCALPHA)
        self.input_boxes = [InputBox(10, 10, 100, 20, globals.get_reward, globals.set_reward),
                    InputBox(10, 40, 100, 20, globals.get_punishment, globals.set_punishment),
                    InputBox(10, 70, 100, 20, globals.get_falloff, globals.set_falloff)]
        self._display_surf = pygame.display.set_mode((MAP_SIZE[0], MAP_SIZE[1]+HUD_HEIGHT))
        self._running = True
        self.spawn_random_lights(NUM_LIGHTS)

    def spawn_random_lights(self, num):
        for x in range(num):
            self.lightSprites.add(LightSprite((math.floor(MAP_SIZE[0] * random.random()), math.floor(MAP_SIZE[1] * random.random())), 255))

    def spawn_nearby_light(self, pos):
        self.lightSprites.add(LightSprite((pos[0] - random.randint(-20, 20), pos[1] - random.randint(-20, 20)), 255))

    def add_lights(self, pos):
        max_dist = math.sqrt((SWARM_SIZE//2)**2 + (SWARM_SIZE//2)**2)
        for x_dist in range(SWARM_SIZE+1):
            x_coord = (pos[0] + x_dist - (SWARM_SIZE//2))
            for y_dist in range(SWARM_SIZE+1):
                y_coord = pos[1] + y_dist - (SWARM_SIZE//2)
                if(x_coord > 0 and y_coord > 0 and x_coord < MAP_SIZE[0] and y_coord < MAP_SIZE[1]):
                    dist_from_center = math.dist((x_coord, y_coord),pos)
                    alpha = int((1-(dist_from_center/max_dist)) * 255)
                    self.lightSprites.add(LightSprite((x_coord, y_coord),alpha))
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_1:
                self.bug.set_move_strat(MoveType.SELF)
            elif event.key == pygame.K_2:
                self.bug.set_move_strat(MoveType.NN)
            elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                self.bug.set_move_strat(MoveType.USER)
                self.bug.move(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            rel_pos = tuple(numpy.subtract(event.pos, (MAP_SIZE[0]//2, MAP_SIZE[1])))
            for box in self.input_boxes:
                box.set_active(rel_pos)
        elif event.type == pygame.KEYDOWN:
            for box in self.input_boxes:
                box.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.add_lights(event.pos)

    def getLight(self, vec):
        for light in self.lightSprites:
            if light.rect.center == self.bug.position + vec:
                return light.surf.get_at((0,0)).r
        return 0

    def on_loop(self):
        self.bug.nn.reinitialize()
        tried_move = self.bug.move()
        self.hud_surf.fill((255,255,255))
        draw_neurons(self.hud_surf, self.bug.nn, False)
        if (tried_move):
            caughtLights = pygame.sprite.spritecollide(self.bug, self.lightSprites, True)
            if len(caughtLights) > 0:
                self.reward_overlay.fill((0,0,0,0))
                draw_neurons(self.reward_overlay, self.bug.nn, True)
                self.bug.eat(caughtLights[0].surf.get_at((0,0)).r/FOOD_MAX)
            else:
                self.bug.eat(0)
        if self.timer == LIGHTS_DELAY:
            self.timer = 0
            self.spawn_nearby_light(self.bug.get_location())
        else:
            self.timer += 1
        #Find all the nearby light values.
        self.bug.light_vals = {key: self.getLight(directions.map[key])/FOOD_MAX for key in directions.map.keys()}

    def on_render(self):
        self._display_surf.fill((0,0,0))
        self._display_surf.blit(self.bug.surf , self.bug.rect)
        for entity in self.lightSprites:
            self._display_surf.blit(entity.surf, entity.rect)
        self.text_surf.fill((128,128,128))
        for box in self.input_boxes:
            box.update()
            box.draw(self.text_surf)
        self.hud_surf.blit(self.text_surf, (MAP_SIZE[0]//2, 0))
        self.reward_overlay.convert_alpha()
        self.hud_surf.blit(self.reward_overlay, (0,0))
        self._display_surf.blit(self.hud_surf, (0, MAP_SIZE[1]))
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()
        self.on_cleanup()

class LightSprite(pygame.sprite.Sprite):
    def __init__(self, pos, alpha):
        super().__init__()
        self.surf = pygame.Surface((1, 1))
        self.surf.fill((alpha,alpha,alpha))
        self.rect = self.surf.get_rect(center = pos)

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
import pygame
from pygame import display
from pygame.locals import *
import sys
from Bug import Bug, MoveType
import math
import Directions as directions

FOOD_MAX = 255
SWARM_SIZE = 20 #best if even
MAP_SIZE = (640, 400)

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = MAP_SIZE
        self.bug = Bug(5, 5, MAP_SIZE)
        self.lightSprites  = pygame.sprite.Group()
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        self._display_surf.fill((0,0,0))
        self._running = True

    def add_lights(self, pos):
        max_dist = math.sqrt((SWARM_SIZE//2)**2 + (SWARM_SIZE//2)**2)
        for x_dist in range(SWARM_SIZE+1):
            x_coord = pos[0] + x_dist - (SWARM_SIZE//2)
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
            self.add_lights(event.pos)

    def getLight(self, vec):
        for light in self.lightSprites:
            if light.rect.center == self.bug.position + vec:
                return light.surf.get_at((0,0)).r
        return 0

    def on_loop(self):
        tried_move = self.bug.move()
        if (tried_move):
            caughtLights = pygame.sprite.spritecollide(self.bug, self.lightSprites, True)
            if len(caughtLights) > 0:
                self.bug.eat(caughtLights[0].surf.get_at((0,0)).r/FOOD_MAX)
            else:
                self.bug.eat(0)
        #Find all the nearby light values.
        self.bug.light_vals = {key: self.getLight(directions.map[key])/FOOD_MAX for key in directions.map.keys()}

    def on_render(self):
        self._display_surf.fill((0,0,0))
        self._display_surf.blit(self.bug.surf , self.bug.rect)
        for entity in self.lightSprites:
            self._display_surf.blit(entity.surf, entity.rect)
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
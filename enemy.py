import pygame
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
SPACE = 4
PotatoPic = pygame.image.load("bad.jpg")
militree = pygame.image.load("GoombaHeadaa.png")

class Goomba():
    def __init__(self, x, y):
        self.xpos = x
        self.ypos = y
        self.direction = 1
        self.vy = 0
        self.isa = True
    def move(self, time,ticker):
        if ticker % 20==0:
            self.xpos+= 1 *self.direction
        return time
    def draw(self, x_offset, y_offset, screen):
        if self.isa == True:
            screen.blit(militree, (self.xpos + x_offset, self.ypos + y_offset))
import pygame
import random

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

class rope:
    def __init__(self):
        self.xpos = 452
        self.ypos = 1222
        self.direction = RIGHT
        self.isOnGround = False
        self.movingx = False
        self.movingy = False
        self.x_offset = 0
        self.y_offset = 0  
    def draw(self, screen, xoff, yoff):
        pygame.draw.(screen, (250, 0, 250), (self.xpos+xoff, self.ypos+yoff), 20)

    def move(self, map, ticker,  px, py, xoff, yoff):
        #check if player is direct line of sight
        #print("y positions in grid:", int(py/50),int(self.ypos/50))
        if int(py/50) == int(self.ypos/50): #check that player and rope are in same row
            if px < self.xpos: #check that player is to the right of rope
                print("I SEE YOU", end = " ")
                if map[int((self.ypos ) / 50)][int( (self.xpos +30 )  / 50)] !=2:
                    self.xpos+=5
            elif px > self.xpos: #left
                if map[int((self.ypos ) / 50)][int( (self.xpos )  / 50)] !=2:
                    self.xpos-=5
       

       
        #you need to expand this for the other directions

        #otherwise randomly wander
        elif ticker%40==0:
            num = random.randrange(0, 4)
            if num == 0:
                self.direction = RIGHT
            elif num == 1:
                self.direction = LEFT
            elif num == 3:
                self.direction = DOWN
     

        if self.isOnGround == False:
            if self.ypos < 810:
                self.vy = 3
            elif self.y_offset > -900:
                self.y_offset-=3
                self.vy = 0
            else:
                self.vy = 3
                self.direction = DOWN
            self.movingy = True
        
        
        
        
        #check for collision and change direction if you've bumped
        if self.direction == RIGHT and map[int((self.ypos ) / 50)][int( (self.xpos +20 )  / 50)] ==2:
            #print("bumped right!")
            self.direction = LEFT
        if self.direction == LEFT and map[int((self.ypos) / 50)][int( (self.xpos - 20 )  / 50)] ==2:
            #print("bumped left!")
            self.direction = RIGHT
        if self.direction == DOWN and map[int((self.ypos) / 50)][int( (self.ypos + 20) / 50)] == 2:
            self.isOnGround = True
        else:
            self.isOnGround = False


        if self.direction == LEFT and self.xpos == 400:
            self.direction = RIGHT
       
#or actually move!
        elif self.direction == RIGHT:
                self.xpos += 5
        elif self.direction == LEFT:
                self.xpos -= 5

#    def enemyCollide(self, xpos, ypos):
#        if self.xpos+20>self.xpos: #right side of player, left side of enemy
#            if self.xpos < self.xpos+20: #left side of player, right side of enemy
#                if self.ypos < self.ypos+20: #top of player bottom of enemy
#                    if self.ypos+20 > self.ypos:
#                        return True
       # else:
            #return False
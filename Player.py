import pygame

#CONSTANTS
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
SPACE = 4

Link = pygame.image.load('link.png') 


class player:
    def __init__(self):
      #player variables
      self.xpos = 50 #xpos of player
      self.ypos = 1600 #ypos of player
      self.vx = 0 #x velocity of player
      self.vy = 0 #y velocity of player
      self.x_offset = 0
      self.y_offset = 0  
      self.isOnGround = False #this variable stops gravity from pulling you down more when on a platform
      self.movingx = False
      self.movingy = False
      #animation variables variables
      self.frameWidth = 32
      self.frameHeight = 46
      self.RowNum = 0 #for left animation, this will need to change for other animations
      self.frameNum = 0
      self.ticker = 0
      self.direction = DOWN
      

    def draw(self,screen, ticker):
        if self.movingx == True or self.movingy == True: #animate when moving
            ticker+=1
        if ticker % 10 == 0: #only change frames every 10 ticks
          self.frameNum+=1
        if self.frameNum > 7: 
           self.frameNum = 0
        screen.blit(Link, (self.xpos, self.ypos), (self.frameWidth * self.frameNum, self.RowNum * self.frameHeight, self.frameWidth, self.frameHeight)) 
        return ticker

    def move(self, keys, map):
        if keys[LEFT] == True:
            if self.xpos > 400:
                self.vx = -3
            elif self.x_offset < 0:
                self.x_offset+=3
                self.vx = 0
            else:
                self.vx = -3
                self.RowNum = 0
                self.direction = LEFT
                self.movingx = True
        
        #RIGHT MOVEMENT
        elif keys[RIGHT] == True:
            if self.xpos < 400:
                self.vx = 3
            elif self.x_offset > -800:
                self.x_offset-=3
                self.vx = 0
            else:
                self.vx = 3
                self.RowNum = 1
                self.direction = RIGHT
                self.movingx = True
        #turn off velocity
        else:
            self.vx = 0
            self.movingx = False
   
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
        #turn off velocity
        else:
            self.vy = 0
            self.movingy = False

         #UP MOVEMENT
        if keys[UP] == True:
            if self.ypos > 400:
                self.vy = -3
            elif self.y_offset < 0:
                self.y_offset+=3
                self.vy = 0
            else:
                self.vy = -3
                self.RowNum = 0
                self.RowNum = 2
                self.direction = UP
                self.movingy = True


        

    
    #COLLISION
    
    #down collision
        if map[int((self.ypos - self.y_offset + self.frameHeight) / 50)][int((self.xpos - self.x_offset + self.frameWidth / 2) / 50)] == 2:
            self.isOnGround = True
        else:
            self.isOnGround = False
    
    #up collision
        if map[int((self.ypos - self.y_offset) / 50)][int((self.xpos - self.x_offset + self.frameWidth / 2) / 50)] == 2:
            self.ypos+=3
        
    #left collision
        if map[int((self.ypos - self.y_offset + self.frameHeight - 10) / 50)][int((self.xpos - self.x_offset - 10) / 50)] == 2 :
            self.xpos+=3
        
    #right collision
        if map[int((self.ypos - self.y_offset) / 50)][int((self.xpos - self.x_offset + self.frameWidth + 5) / 50)] == 2:
            self.xpos-=3    

    #stop moving if you hit edge of screen (will be removed for scrolling)
        if self.xpos + self.frameWidth > 800:
            self.xpos-=3
        if self.xpos < 0:
            self.xpos+=3

        self.xpos+=self.vx #update player xpos
        self.ypos+=self.vy
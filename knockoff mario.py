import pygame
import math


pygame.init()  
pygame.display.set_caption("Knockoff Mario")
screen = pygame.display.set_mode((832, 900))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() #set up clock
gameover = False #variable to run our game loop
end = False

#CONSTANTS
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
SPACE = 4
ye = print("Yuh Brandon cute😂")
potato = True

#images
dartD = pygame.image.load('dart-down.png')
dartU = pygame.image.load('dart-up.png')
dartR = pygame.image.load('dart-right.png')
dartL = pygame.image.load('dart-left.png')
brick = pygame.image.load('brick.png') #load your spritesheet
dirt = pygame.image.load('bad.jpg')
Link = pygame.image.load('link.png') #load your spritesheet
PotatoPic = pygame.image.load("bad.jpg")
Link.set_colorkey((255, 0, 255)) #this makes bright pink (255, 0, 255) transparent (sort of)
militree = pygame.image.load("GoombaHeadaa.png")

keys = [False, False, False, False, False] #this list holds whether each key has been pressed


#enemy Variables
timer = 0

#Player Class
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
      self.lives = 3
      

    def draw(self,screen, ticker):
        if self.lives > 0:
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

         #UP MOVEMENT
        elif keys[UP] == True and self.isOnGround == True:
            if self.ypos > 400:
                self.vy = -50
            elif self.y_offset < 0:
                self.y_offset+=50
                self.vy = 0
            else:
                self.vy = -50
            self.RowNum = 0
            self.RowNum = 2
            self.direction = UP
            self.movingy = True
        #turn off velocity
        else:
            self.vy = 0
            self.movingy = False


        

    
    #COLLISION
    
    #down collision
        if map[int((self.ypos - self.y_offset + self.frameHeight) / 50)][int((self.xpos - self.x_offset + self.frameWidth / 2) / 50)] == 2:
            self.isOnGround = True
        else:
            self.isOnGround = False
    
    #up collision
        if map[int((self.ypos - self.y_offset) / 50)][int((self.xpos - self.x_offset + self.frameWidth / 2) / 50)] == 2:
            self.vy+=3
        
    #left collision
        if map[int((self.ypos - self.y_offset + self.frameHeight - 10) / 50)][int((self.xpos - self.x_offset - 10) / 50)] == 2 :
            self.vx+=3
        
    #right collision
        if map[int((self.ypos - self.y_offset) / 50)][int((self.xpos - self.x_offset + self.frameWidth + 5) / 50)] == 2:
            self.vx-= 4

    #stop moving if you hit edge of screen (will be removed for scrolling)
        if self.xpos + self.frameWidth > 800:
            self.xpos-=3
        if self.xpos < 0:
            self.xpos+=3

        self.xpos+=self.vx #update player xpos
        self.ypos+=self.vy
    
    def ecollide(self, goombax, goombay):
        if self.lives > 0:
            if goombax > self.xpos:
                if goombax < self.xpos + self.x_offset:
                    if goombay > self.ypos + self.y_offset:
                        if goombay < self.ypos:
                            self.lives -= 1
                            return self.lives


class Goomba():
    def __init__(self, x, y):
        self.xpos = 700
        self.ypos = 875
        self.direction = 1
        self.vy = 0
        self.isa = True
    def move(self, time):
        if ticker % 20==0:
            self.xpos+= 1 *self.direction
        return time
    def draw(self, x_offset, y_offset):
        if self.isa == True:
            screen.blit(militree, (self.xpos + x_offset, self.ypos + y_offset))


cBASS = Goomba(20,60)

class fireball:
    def __init__(self):
        self.xpos = -10 #draw offscreen when not in use
        self.ypos = -10
        self.isAlive = False
        self.direction = RIGHT
    def shoot(self, x, y, dir):
        self.xpos = x + 20
        self.ypos = y + 20
        self.isAlive = True
        self.direction = dir
        
    def move(self):
        if self.direction == RIGHT:
            self.xpos+=20
        elif self.direction == LEFT:
            self.xpos-=20
        elif self.direction == UP:
            self.ypos-=20
        elif self.direction == DOWN:
            self.ypos+=20
    
        #add other directions here
    def draw(self):
        if self.direction == LEFT:
            screen.blit(dartL, (self.xpos, self.ypos))
        elif self.direction == RIGHT:
            screen.blit(dartR, (self.xpos, self.ypos))
        elif self.direction == UP:
            screen.blit(dartU, (self.xpos, self.ypos))
        elif self.direction == DOWN:
            screen.blit(dartD, (self.xpos, self.ypos))
        
    def collide(self, x, y):
        if math.sqrt((self.xpos - x) ** 2 + (self.ypos - y) ** 2) < 25: #25 is radius of fireball + radius of potato
            print("collision!")
            return True
        
        elif math.sqrt((self.xpos - x) ** 2 + (self.ypos - y) ** 2) == 2: #25 is radius of fireball + radius of potato
            print("collision!")
            return True
        else:
            return False
       

ball = fireball()

#MAP: 1 is grass, 2 is brick
map = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 ,2 ,2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 ,2 ,2, 2, 2],
       [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2 ,2 ,2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 2, 2 ,2 ,2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0 ,0 ,0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0 ,0 ,0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0 ,0 ,0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 2, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,2, 2, 2, 0, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 2 ,0 ,0, 0, 2],
       [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,2 ,2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2 ,2 ,0, 0, 2],
       [2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 2, 2],
       [2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,2 ,2, 2, 2],
       [2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0 ,0 ,2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2 ,2 ,2, 2, 2],
       [2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 2 ,2 ,2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 2, 2, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 2, 2, 2, 0, 2, 2, 0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0 ,0 ,0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2 ,0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0 ,0 ,0, 0, 2],
       [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2 ,2 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0 ,0 ,0, 0, 2],
       [2, 2, 2, 2, 2, 2, 2, 0, 0, 1, 0, 0, 0 ,2 ,2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2 ,0 ,0, 0, 2],
       [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2 ,2 ,2, 2, 2],
       [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2 ,2 ,2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2 ,2 ,2, 2, 2],
       [2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2 ,2 ,2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2 ,2 ,2, 2, 2],
       [2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2 ,2 ,2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 ,2 ,2, 2, 2],
       [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 ,2 ,2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 ,2 ,2, 2, 2]]




p1 = player()

#animation variables variables
frameWidth = 32
frameHeight = 46
RowNum = 0 #for left animation, this will need to change for other animations
frameNum = 0
ticker = 0
direction = DOWN

while not gameover:
    clock.tick(60) #FPS
    timer +=1
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True
     
        if event.type == pygame.KEYDOWN: #keyboard input
            if event.key == pygame.K_LEFT:
                keys[LEFT] = True
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT] = True
            elif event.key == pygame.K_UP:
                keys[UP] = True
            elif event.key == pygame.K_DOWN:
                keys[DOWN] = True
            elif event.key == pygame.K_SPACE:
                keys[SPACE] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys[LEFT] = False
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT] = False
            elif event.key == pygame.K_UP:
                keys[UP] = False
            elif event.key == pygame.K_DOWN:
                keys[DOWN] = False
            elif event.key == pygame.K_SPACE:
                keys[SPACE] = False
         


    #check space for shooting
    if keys[SPACE] == True:
        ball.shoot(p1.xpos, p1.ypos, p1.direction)
       
    ball.move()




    if cBASS.isa == True:
        p1.ecollide(cBASS.xpos, cBASS.ypos)

    #DOWN MOVEMENT
    #if keys[DOWN] == True:
        #if ypos < 400:
         #   vy = 3
        #elif y_offset > -900:
          #  y_offset-=3
           # vy = 0
        #else:
        #    vy = 3
        #RowNum = 1
        #RowNum = 3
        #direction = DOWN
        #movingy = True

         # MOVEMENT







    #ANIMATION-------------------------------------------------------------------
       
    # Update Animation Information

    if p1.movingx == True or p1.movingy == True: #animate when moving
        ticker+=1
        if ticker % 10 == 0: #only change frames every 10 ticks
          frameNum+=1
        if frameNum > 7:
           frameNum = 0
 
    if p1.xpos > 386 and p1.xpos < 400 and p1.ypos < 160 and p1.ypos > 50:
        gameover = True
        
    if p1.lives <= 0:
        gameover = True
            
    # RENDER--------------------------------------------------------------------------------
    # Once we've figured out what frame we're on and where we are, time to
    # render.



    p1.move(keys, map)

           
    screen.fill((66, 165, 245)) #wipe screen so it doesn't smear
   
    #draw map
    for i in range(34):
        for j in range(33):
            if map[i][j] == 1:
                screen.blit(dirt, (j * 50 + p1.x_offset, i * 50 + p1.y_offset), (0, 0, 50, 50))
            if map[i][j] == 2:
                screen.blit(brick, (j * 50 + p1.x_offset, i * 50 + p1.y_offset), (0, 0, 50, 50))
   
    #draw fireball
    if ball.isAlive == True:
        ball.draw()
    #draw player
    p1.draw(screen, ticker)
    #draw potato
    if potato == True:
        screen.blit(PotatoPic, (200 + p1.x_offset, 200 + p1.y_offset))
    

    #Draw Goomba
    cBASS.draw(p1.x_offset, p1.y_offset)
   
    #Move Goomba
    cBASS.move(timer)


    pygame.display.flip()#this actually puts the pixel on the screen


#end game
#loop------------------------------------------------------------------------------
#pygame.quit()


#END GAME SCREEN IF U WANT---------------------------------------------
#import pygame
#import random
#import math
#pygame.init()  
#pygame.display.set_caption("EEL")  # sets the window title
#screen = pygame.display.set_mode((1000, 1000))  # creates game screen
#screen.fill((0,0,0))
#clock = pygame.time.Clock() #set up clock

#while not end:
#    screen.fill((0,0,255))
#    font = pygame.font.Font(None, 65)
#    text = font.render(str("YOU WIN"),1, (255,255,255))
#    screen.blit(text, (435, 435))
#    pygame.display.flip()
#pygame.quit()


""" blocker.py - Copyright 2019 Arin  """
## air == 0
## dirt == 1
## grass == 2
## cloud == 3

import sys
from random import randint
import pygame
from pygame.locals import Rect, QUIT, KEYDOWN, \
    K_a, K_d, K_w, MOUSEBUTTONDOWN, KEYUP, K_LALT, MOUSEMOTION, K_v
pygame.init()
pygame.key.set_repeat(5, 5)
Width = 800
Height = 400
W = int(Width/50)
H = int(Height/50)
SURFACE = pygame.display.set_mode((Width, Height+50))
FPSCLOCK = pygame.time.Clock()
BLOCKS = [[0 for _ in range(W)] for _ in range(H)]
player = pygame.image.load("player1.png")
image_player = pygame.Surface((25, 50))
sprite = pygame.image.load("strip.png")
image = pygame.Surface((50, 50))
pygame.key.get_pressed()
sysfont = pygame.font.SysFont(None, 20)

class BLOCK:
    #Blcok class
    def __init__(self, x, y, code):
        self.x = x
        self.y = y
        self.code = code


    def draw(self):
        image.blit(sprite, (0,0), Rect(self.code * 50, 0, 50, 50))
        SURFACE.blit(image, (self.x, self.y))


class PLAYER:
    #Player class
    v = 7
    m = 1
    isjump = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = [0, 0, 0, 0]
        self.inv = 0

    def move(self, tmpx):
        self.x += tmpx
        #LEFT
        block = BLOCKS[int((self.y+49)/50)][int((self.x+5)/50)-1]
        if not block.code == 0:
            if self.x <= block.x+50:
                self.x = block.x+50
                
        #RIGHT
        block = BLOCKS[int((self.y+49)/50)][int(self.x/50) +1]
        if not block.code == 0:
            if self.x+25 > block.x:
                self.x = block.x-25
    
        if self.x <= 0:
            self.x = 0
        if self.x >= Width-20:
            self.x = Width-25

        
    def draw(self):
        if self.isjump == 1:
            # Calculate force (F). F = 0.5 * mass * velocity^2.
            if self.v > 0:
                F = ( 0.5 * self.m * (self.v*self.v) )
            else:
                F = -( 0.5 * self.m * (self.v*self.v) )


            # Change position
            self.y = self.y - F

            # Change velocity
            self.v = self.v - 1


            self.iscollide()


                
        
        image_player.blit(player, (0, 0), Rect(0, 0, 25, 50))
        SURFACE.blit(image_player, (self.x, self.y))
        

    
    def iscollide(self):

        #DOWN
        block = BLOCKS[int((self.y+50)/50)][int(self.x/50)]
        if not block.code == 0:
            if self.y+50 > block.y:
                self.y = block.y-50
                self.v = 7
                self.isjump = 0

        block = BLOCKS[int((self.y+50)/50)][int((self.x+24)/50)]
        if not block.code == 0:
            if self.y+50 > block.y:
                self.y = block.y-50
                self.v = 7
                self.isjump = 0

        #UP
        block = BLOCKS[int((self.y+50)/50 -1)][int(self.x/50)]
        if not block.code == 0:
            if self.y > block.y:
                self.y = block.y+50

        block = BLOCKS[int((self.y+50)/50)-1][int((self.x+24)/50)]
        if not block.code == 0:
            if self.y > block.y:
                self.y = block.y+50



    def jump(self):
        self.isjump = 1


    def display(self):
        #range
        x = int(self.x/50)
        tmpx = x - 50
        tmpy = self.y - 50

        for yy in range(tmpy, tmpx+100, 50):
            for xx in range(tmpx, tmpx+100, 50):
                pygame.draw.rect(SURFACE, (255, 0, 0), ((xx, yy), (50, 50)), 3)

    def Place(self, focus):
        xx, yy = focus
        #place
        if not ((int(xx/50)*50 == int(self.x/50)*50 and\
            int(yy/50)*50 == int(self.y/50)*50) or\
            (int(xx/50)*50 == int((self.x+24)/50)*50 and\
            int(yy/50)*50 == int(self.y/50)*50)):

            block = BLOCKS[int(yy/50)][int(xx/50)]
            if block.code == 0:
                #have block
                if not self.inventory[self.inv] == 0:
                    
                    block.code = self.inv
                    self.inventory[self.inv] -= 1
                    BLOCKS[int(yy/50)][int(xx/50)] = block
            

    def Break(self, focus):
        xx, yy = focus
        #break
        if not (int(xx/50)*50 == int(self.x/50)*50 and\
            int(yy/50)*50 == int(self.y/50)*50 ):
            
            block = BLOCKS[int(yy/50)][int(xx/50)]
            if not block.code == 0:
                self.inventory[block.code] += 1
                block.code = 0
                BLOCKS[int(yy/50)][int(xx/50)] = block
            

    def Inventory(self):
        #background
        for xx in range(0, Width, 50):
            pygame.draw.rect(SURFACE, (73, 73, 73), ((xx, Height), (50, 50)))

        #blocks
        for xx in range(len(self.inventory)):
            image.blit(sprite, (0,0), Rect(xx * 50, 0, 50, 50))
            SURFACE.blit(image, (xx*50, Height))
            score_image = sysfont.render("{}".format(self.inventory[xx]), True, (0, 0, 0))
            SURFACE.blit(score_image, (xx*50 + 35, Height+35))

        #line
        for xx in range(0, Width, 50):
            pygame.draw.rect(SURFACE, (40, 40, 40), ((xx, Height), (50, 50)), 5)
            
        pygame.draw.rect(SURFACE, (255, 255, 255), ((self.inv*50, Height), (50, 50)), 3)
        
    
def main():
    display = 0
    mousepos = None
    Player = PLAYER(int(Width/2), int(200))
    inv = 0
    #fill air
    for y in range(0, H):
        for x in range(0, W):
            BLOCKS[y][x] = BLOCK(x*50, y*50, 0)

    for y in range(int(H - H/4), H):
        for x in range(0, W):
            BLOCKS[y][x] = BLOCK(x*50, y*50, 1)

    BLOCKS[5][3] = BLOCK(3*50, 5*50, 1)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LALT:
                    display = 1

                elif event.key == 48:
                    Player.inv = 9
                elif event.key > 48 and event.key <58:
                    Player.inv = event.key - 48 -1

                if event.key == K_v:
                    for i in range(len(Player.inventory)):
                        Player.inventory[i] += 1
                    
            elif event.type == KEYUP:
                if event.key == K_LALT:
                    display = 0
            elif event.type == MOUSEMOTION:
                mousepos = event.pos
                

            elif event.type == MOUSEBUTTONDOWN:
                #Left button
                if event.button == 1: 
                    Player.Break(focus)

                #Right button
                elif event.button == 3:
                    Player.Place(focus)
                    
                
        keys = pygame.key.get_pressed()
        if (keys[K_a]):
            Player.move(-5)

        if (keys[K_d]):
            Player.move(+5)
            
        if (keys[K_w]):
            Player.jump()

        #Gravity
        if not Player.isjump:
            Player.y += 10
        Player.iscollide()
    
        
        #grass check:
        for x in range(W):
            for y in range(H):
                block = BLOCKS[y][x]
                if not y == 0:
                    if block.code == 1: # dirt
                        if BLOCKS[y-1][x].code == 0:
                            block.code = 2
                            BLOCKS[y][x] = block

        #BlockDraw
        for y in range(H):
            for x in range(W):
                block = BLOCKS[y][x]
                block.draw()
                    
        #focus
        xx, yy = mousepos
        xx = int(xx/50) * 50
        yy = int(yy/50) * 50
        if yy >= Height-50:
            yy = Height-50
        
        pygame.draw.rect(SURFACE, (255, 0, 0), ((xx, yy), (50, 50)), 2)
        focus = (xx, yy)
        
        if display == 1:
            x = int((Player.x+17.5)/50) * 50
            y = int((Player.y+25)/50) * 50
            tmpx = x - 50
            tmpy = y - 50
            for yy in range(tmpy, tmpy+100+1, 50):
                for xx in range(tmpx, tmpx+100+1, 50):
                    pygame.draw.rect(SURFACE, (255, 0, 0), (xx, yy, 50, 50), 3)
        #PlayerDraw
        Player.draw()
        Player.Inventory()
        pygame.display.update()
        FPSCLOCK.tick(30)

if __name__ == '__main__':
    main()

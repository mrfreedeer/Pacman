import pygame
import json
import math
from pygame.locals import *
from sys import exit


red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

class Jugador(pygame.sprite.Sprite):
    def __init__(self,ancho, alto, dock, tile, startx, starty, path):
        pygame.sprite.Sprite.__init__(self)
        self._d = dock
        self._t = tile
        self.image = path
        self.rect = self.image.get_rect()
        self.rect.x = startx
        self.rect.y = starty
        self.x = 0
        self.y = 0
        self.posx = startx
        self.posy = starty
        #self.image.fill(pink)
    def changeimage(self, ancho, alto, path):
        image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(image, (ancho,alto))
        self.rect = self.image.get_rect()
        self.rect.x = self.posx
        self.rect.y = self.posy
    def update(self, mazesprites, width):
        ls_col = pygame.sprite.spritecollide(self, mazesprites, False)
        cols = False
        for colision in ls_col:
            cols = True
            if self.x> 0:
                self.rect.right = colision.rect.left
            if self.x< 0:
                self.rect.left = colision.rect.right
        self.posx = self.rect.x

        for colision in ls_col:
            if self.y > 0:
                self.rect.bottom = colision.rect.top
            if self.y < 0:
                self.rect.top = colision.rect.bottom
        self.posy = self.rect.y

        if self.posx < (self._d[0] - self._t + 5):
            self.posx =  self._d[0] + self._t * (width -1)
            self.rect.x = self._d[0] + self._t * (width -1)
        if self.posx > self._d[0] + self._t * (width - 1)  :
            self.posx = self.rect.x = self._d[0]

class Wall (pygame.sprite.Sprite):
    def __init__(self, x, y, tilesize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tilesize, tilesize))
        self.image.fill(blue)
        self.rect = self.image.get_rect(x = x, y = y)
class Xline (pygame.sprite.Sprite):
    def __init__(self, x, y, tilesize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tilesize, 1))
        self.image.fill(blue)
        self.rect = self.image.get_rect(x = x, y = y)
class Yline (pygame.sprite.Sprite):
    def __init__(self, x, y, length):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, length))
        self.image.fill(blue)
        self.rect = self.image.get_rect(x = x, y = y)



def readmaze(string):
    json_data = open(string).read().split("\n")
    return json_data
class Maze(pygame.sprite.Sprite):
    def __init__(self, string, free, height, DOCK):
        pygame.sprite.Sprite.__init__(self)

        self._d = DOCK
        self._mazemap = readmaze(string)
        self._width = len(self._mazemap[0])
        self._height = len(self._mazemap) - 1
        self._t = math.ceil(abs((height - free)) / self._height)
        #self._t = abs((height - free)) / self._height
        self._walls = []
        self._lines = []
        self._sprites = pygame.sprite.Group()

    def getTile(self):
        return self._t
    def getWidth(self):
        return self._width
    def outline(self, pantalla):
        self._lines.append(Xline(self._d[0] - 1, self._d[1] - 1, self._width * self._t))
        self._lines.append(Xline(self._d[0] - 1, self._height*self._t + self._d[1] +self._t,self._width * self._t ))

        self._lines.append(Yline(self._d[0] -1 , self._d[1],self._t * 6))

        self._lines.append(Yline(self._d[0] + self._width * self._t, self._d[1],self._t * 6))

        self._lines.append(Yline(self._d[0] -1 , self._d[1] + 13 * self._t,self._t * 7))
        self._lines.append(Yline(self._d[0] + self._width * self._t, self._d[1] + 13 * self._t, self._t * 7))


        self._lines.append(Yline(self._d[0] - 1 +  3 * self._t, self._d[1]+ 6 * self._t ,3 * self._t - 1))
        self._lines.append(Yline(self._d[0] + 14 * self._t, self._d[1]+ 6 * self._t,3 * self._t - 1))

        self._lines.append(Yline(self._d[0] - 1 + 3 * self._t, self._d[1]+ 10 * self._t,3 * self._t - 1))
        self._lines.append(Yline(self._d[0] + 14 * self._t, self._d[1]+ 10 * self._t,3 * self._t - 1))


        self._lines.append(Yline(self._d[0] + 6 * self._t, self._d[1] + 8 * self._t, 3 * self._t - 1))
        self._lines.append(Yline(self._d[0] - 1 + 11 * self._t, self._d[1] + 8 * self._t,  3 * self._t - 1))

        self._lines.append(Xline(self._d[0] - 1, self._d[1] + 6 * self._t, 3 * self._t))
        self._lines.append(Xline(self._d[0] + 1 + self._t * (self._width - 3) , self._d[1]  + 6 * self._t, 3 * self._t))
        self._lines.append(Xline(self._d[0], self._d[1] + 9 * self._t - 1, self._t * 3 ))
        self._lines.append(Xline(self._d[0], self._d[1] + 10 * self._t , self._t * 3 ))

        self._lines.append(Xline(self._d[0] + self._t * (self._width - 3), self._d[1] + 9 * self._t - 1, self._t * 3 ))
        self._lines.append(Xline(self._d[0]+ self._t * (self._width - 3), self._d[1] + 10 * self._t, self._t * 3 ))
        self._lines.append(Xline(self._d[0] + 1 + 6 * self._t, + self._d[1] + 8 * self._t, 2 * self._t))
        self._lines.append(Xline(self._d[0] + 9 * self._t, + self._d[1] + 8 * self._t, 2 * self._t))
    def draw(self, pantalla):
        self.outline(pantalla)
        for row in range(self._height):
            for col in range(self._width):
                if self._mazemap[row][col] == '1' :
                    self._walls.append(Wall(col*self._t + self._d[0], row*self._t + self._d[1], self._t))
                if self._mazemap[row][col] == '0' :
                    pass
                if self._mazemap[row][col] == '3':
                    self._lines.append(Xline(col*self._t + self._d[0], row*self._t + self._d[1] - 1, self._t))
        for x in self._walls:
            self._sprites.add(x)
        for y in self._lines:
            self._sprites.add(y)
        self._sprites.draw(pantalla)
        z = Yline(self._d[0] - self._t - 5, self._d[1], self._t * self._height)
        z1 = Yline(self._d[0] + self._t * (self._width + 1) + 5, self._d[1], self._t * self._height)
        z2 = Xline(self._d[0] + 8 * self._t, self._d[1] + 8 * self._t, self._t)
        self._sprites.add(z)
        self._sprites.add(z1)
    def getSprites(self):
        return self._sprites

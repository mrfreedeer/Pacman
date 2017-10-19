import pygame
import json
from pygame.locals import *
from sys import exit


red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

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



def readmaze():
    json_data = open("C:\\Users\\Usuario1\\Desktop\\Pacman-master\\Pacman-master\\maze.txt").read().split("\n")
    return json_data
class Maze(pygame.sprite.Sprite):
    def __init__(self, TILESIZE, DOCK):
        pygame.sprite.Sprite.__init__(self)
        self._t = TILESIZE
        self._d = DOCK
        self._mazemap = readmaze()
        self._width = len(self._mazemap[0])
        self._height = len(self._mazemap) - 1
        self._walls = []
        self._lines = []
        self._sprites = pygame.sprite.Group()
         

    def outline(self, pantalla):
        self._lines.append(Xline(self._d[0], self._d[1], self._width * self._t))
        self._lines.append(Xline(self._d[0], self._height*self._t + self._d[1] +self._t,self._width * self._t ))
        self._lines.append(Yline(self._d[0], self._d[1],self._t * 6))
        self._lines.append(Yline(self._d[0] + self._width * self._t, self._d[1],self._t * 6))
        self._lines.append(Yline(self._d[0], self._d[1] + 13 * self._t,self._t * 20))
        self._lines.append(Yline(self._d[0] + self._width * self._t, self._d[1] + 13 * self._t, self._t * 20))

        self._lines.append(Yline(self._d[0] + 3 * self._t, self._d[1]+ 6 * self._t,9 * self._t))
        self._lines.append(Yline(self._d[0] + 3 * self._t, self._d[1]+ 10 * self._t,13 * self._t))

        self._lines.append(Yline(self._d[0] + (self._width - 3) * self._t, self._d[1]+ 6 * self._t,9 * self._t))
        self._lines.append(Yline(self._d[0] + (self._width - 3) * self._t, self._d[1]+ 10 * self._t, 13 * self._t))

        self._lines.append(Yline(self._d[0] + 6 * self._t, self._d[1] + 8 * self._t, 11 * self._t))
        self._lines.append(Yline(self._d[0] + 11 * self._t, self._d[1] + 8 * self._t,  11 * self._t))
    
    def draw(self, pantalla):
        self.outline(pantalla)
        for row in range(self._height):
            for col in range(self._width):
                if self._mazemap[row][col] == '1' :
                    #pygame.draw.rect(pantalla, blue,(col*self._t + self._d[0], row*self._t + self._d[1], self._t, self._t))
                    self._walls.append(Wall(col*self._t + self._d[0], row*self._t + self._d[1], self._t)) 
                if self._mazemap[row][col] == '0' :
                    pass
                if self._mazemap[row][col] == '3':
                    #pygame.draw.line(pantalla,blue,(col*self._t + self._d[0], row*self._t + self._d[1]), (col*self._t + self._d[0] + self._t,row*self._t + self._d[1]), 1)
                    self._lines.append(Xline(col*self._t + self._d[0], row*self._t + self._d[1], self._t))
        for x in self._walls:
            self._sprites.add(x)
        for y in self._lines:
            self._sprites.add(y)
        self._sprites.draw(pantalla)

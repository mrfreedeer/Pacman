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

def readmaze():
    json_data = open("/home/juan/Escritorio/Project/maze.txt").read().split('\n')
    return json_data

class Maze(object):
    def __init__(self, TILESIZE, DOCK):
        self._t = TILESIZE
        self._d = DOCK
        self._mazemap = readmaze()
        self._width = len(self._mazemap[0])
        self._height = len(self._mazemap) - 1

    def outline(self, pantalla):
        pygame.draw.line(pantalla,blue,(self._d[0], self._d[1]), (self._width * self._t + self._d [0], self._d[1]), 1)
        pygame.draw.line(pantalla,blue,(self._d[0], self._height*self._t + self._d[1] +self._t), (self._width * self._t + self._d [0], self._t + self._height*self._t + self._d[1]), 1)
        pygame.draw.line(pantalla,blue, (self._d[0], self._d[1]), (self._d[0],self._d[1] + self._t * 6), 1)
        pygame.draw.line(pantalla,blue, (self._d[0] + self._width * self._t, self._d[1]), (self._d[0] + self._width * self._t,self._d[1] + self._t * 6), 1)

        pygame.draw.line(pantalla,blue, (self._d[0], self._d[1] + 13 * self._t), (self._d[0],self._d[1] + self._t * 20), 1)
        pygame.draw.line(pantalla,blue, (self._d[0] + self._width * self._t, self._d[1] + 13 * self._t), (self._d[0] + self._width * self._t,self._d[1] + self._t * 20), 1)

        pygame.draw.line(pantalla, blue, (self._d[0] + 3 * self._t, self._d[1]+ 6 * self._t),(self._d[0] + 3 * self._t, self._d[1]+ 9 * self._t),1)
        pygame.draw.line(pantalla, blue, (self._d[0] + 3 * self._t, self._d[1]+ 10 * self._t),(self._d[0] + 3 * self._t, self._d[1]+ 13 * self._t),1)

        pygame.draw.line(pantalla, blue, (self._d[0] + (self._width - 3) * self._t, self._d[1]+ 6 * self._t),(self._d[0] + (self._width - 3) * self._t, self._d[1]+ 9 * self._t),1)
        pygame.draw.line(pantalla, blue, (self._d[0] + (self._width - 3) * self._t, self._d[1]+ 10 * self._t),(self._d[0] + (self._width - 3) * self._t, self._d[1]+ 13 * self._t),1)

        pygame.draw.line(pantalla, blue, (self._d[0] + 6 * self._t, self._d[1] + 8 * self._t), (self._d[0] + 6 * self._t, self._d[1] + 11 * self._t), 1)
        pygame.draw.line(pantalla, blue, (self._d[0] + 11 * self._t, self._d[1] + 8 * self._t), (self._d[0] + 11 * self._t, self._d[1] + 11 * self._t), 1)

    def draw(self, pantalla):
        self.outline(pantalla)
        for row in range(self._height):
            for col in range(self._width):
                if self._mazemap[row][col] == '1' :
                    pygame.draw.rect(pantalla, blue,(col*self._t + self._d[0], row*self._t + self._d[1], self._t, self._t))
                if self._mazemap[row][col] == '0' :
                    pass
                if self._mazemap[row][col] == '3':
                    pygame.draw.line(pantalla,blue,(col*self._t + self._d[0], row*self._t + self._d[1]), (col*self._t + self._d[0] + self._t,row*self._t + self._d[1]), 1)
                if self._mazemap[row][col] == '4':
                    if col > self._width/2:
                        pygame.draw.line(pantalla,blue,(col* self._t + self._d[0] + self._t, row*self._t + self._d[1]), (col * self._t + self._d [0] + self._t, row*self._t + self._d[1] + self._t), 1)
                    else:
                        pygame.draw.line(pantalla,blue,(col* self._t + self._d[0], row*self._t + self._d[1]), (col * self._t + self._d [0], row*self._t + self._d[1] + self._t), 1)

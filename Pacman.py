import pygame
from maze import Maze
from pygame.locals import *

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
TILESIZE = 31

if __name__ == '__main__':
    pygame.init()
    screensize = pygame.display.Info()
    pantalla = pygame.display.set_mode([screensize.current_w,screensize.current_h])
    x = (screensize.current_w / 2 ) - (8.5 * TILESIZE)
    y = (screensize.current_h / 2) - (11 * TILESIZE)
    DOCK = (x,y)
    pygame.display.set_caption('PAC-MAN')
    pantalla.fill(black)
    mazelocation = "/home/juan/Escritorio/Project/maze.txt"
    m = Maze(mazelocation, 200, screensize.current_h, DOCK)
    m.draw(pantalla)
    mazesprites = m.getSprites()

    while True:
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

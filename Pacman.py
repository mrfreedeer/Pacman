import pygame
import math
from maze import *
from pygame.locals import *

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)


def movement(key, speed):
    if key == pygame.K_RIGHT:
        jp.rect.x += speed
        jp.posx += speed
    if key == pygame.K_LEFT:
        jp.rect.x -= speed
        jp.posx -= speed
    if key == pygame.K_UP:
        jp.rect.y -= speed
        jp.posy -= speed
    if key == pygame.K_DOWN:
        jp.rect.y += speed
        jp.posy += speed
def changedir(key, playershadow, jp):
    if key == pygame.K_RIGHT:
        move = True
        playershadow.x = 5
        playershadow.y = 0
        playershadow.rect.x = jp.rect.x + 1
        playershadow.rect.y = jp.rect.y
    elif key == pygame.K_LEFT:
        move = True
        playershadow.x = -5
        playershadow.y = 0
        playershadow.rect.x = jp.rect.x - 1
        playershadow.rect.y = jp.rect.y
    elif key == pygame.K_UP:
        move = True
        playershadow.y = -5
        playershadow.x = 0
        playershadow.rect.x = jp.rect.x
        playershadow.rect.y = jp.rect.y - 1
    elif key == pygame.K_DOWN:
        move = True
        playershadow.y = 5
        playershadow.x = 0
        playershadow.rect.x = jp.rect.x
        playershadow.rect.y = jp.rect.y + 1
def updatemain(jp, mantain):
    if mantain == pygame.K_RIGHT:
        jp.x = 5

    elif mantain == pygame.K_LEFT:
        jp.x = -5
    elif mantain == pygame.K_UP:
        jp.y = -5
    elif mantain == pygame.K_DOWN:
        jp.y = 5

    if mantain == pygame.K_DOWN or mantain == pygame.K_UP:
        jp.x = 0
    elif mantain == pygame.K_LEFT or mantain == pygame.K_RIGHT:
        jp.y = 0

if __name__ == '__main__':
    pygame.init()
    FREE = 200
    screensize = pygame.display.Info()
    pantalla = pygame.display.set_mode([screensize.current_w,screensize.current_h])
    mazelocation = "/home/juan/Escritorio/Project/maze.txt"
    maze = readmaze(mazelocation)
    TILESIZE = math.ceil(abs((screensize.current_h - FREE)) /(len(maze) - 1) )
    clock = pygame.time.Clock()
    x = (screensize.current_w / 2 ) - (8.5 * TILESIZE)
    y = (screensize.current_h / 2) - (11 * TILESIZE)
    DOCK = (x,y)
    pygame.display.set_caption('PAC-MAN')
    pantalla.fill(black)
    m = Maze(mazelocation, FREE, screensize.current_h, DOCK)
    m.draw(pantalla)
    mazesprites = m.getSprites()
    playersize = int(TILESIZE)
    startx = DOCK[0] + (8 * TILESIZE)
    starty = DOCK[1] + 15 * TILESIZE

    image = pygame.image.load('Pacmanc.png').convert_alpha()
    closedpac = pygame.transform.scale(image, (playersize,playersize))
    image = pygame.image.load('Pacmanright.png').convert_alpha()
    rightpac = pygame.transform.scale(image, (playersize,playersize))
    image = pygame.transform.rotate(image, 90)
    uppac = pygame.transform.scale(image, (playersize,playersize))
    image = pygame.transform.rotate(image, 90)
    leftpac = pygame.transform.scale(image, (playersize,playersize))
    image = pygame.transform.rotate(image, 90)
    downpac = pygame.transform.scale(image, (playersize,playersize))
    currentpac = leftpac

    jp = Jugador(playersize,playersize, DOCK, TILESIZE, startx, starty, currentpac)
    playershadow = Jugador(playersize,playersize, DOCK, TILESIZE, startx, starty, currentpac)
    g = pygame.sprite.GroupSingle()
    g.add(jp)

    ancholab = m.getWidth() + DOCK[0]
    limitancho = ancholab * m.getTile()
    quit = eating = collision = pendingturn = False
    speed  = 1
    magic = pygame.Surface((TILESIZE,3 * TILESIZE))
    magic.fill(black)
    key = None
    turn = 0
    turnspeed = speed * 2
    mouthchange = False
    closed = False

    start = move = True

    mantain = pygame.K_LEFT
    updatemain(jp, mantain)


    counter = 0


    while True:
        pygame.draw.rect(pantalla, black, (jp.posx, jp.posy, playersize, playersize) )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                quit = True
        if event.type == pygame.KEYDOWN:
            key = event.key
            changedir(key, playershadow, jp)
            collision = False
            ls = pygame.sprite.spritecollideany(playershadow, mazesprites, False)
            if ls != None:
                collision = True
                if mantain != key:
                    pendingturn = True

            if not collision:
                mantain = key
                pendingturn = False
                updatemain(jp,mantain)
                if key == pygame.K_RIGHT:
                    currentpac = rightpac
                elif key == pygame.K_LEFT:
                    currentpac = leftpac
                elif key == pygame.K_UP:
                    currentpac = uppac
                elif key == pygame.K_DOWN:
                    currentpac = downpac



        if move and turn >= turnspeed or start:
            start = False
            if eating:
                realspeed = speed * .5
            elif (jp.posx < DOCK[0] + 2 * TILESIZE or jp.posx > DOCK[0] + (m.getWidth() - 4) * TILESIZE) and (jp.posy >= TILESIZE * 10 and jp.posy <= TILESIZE * 11):
                realspeed = speed * 1.5
            else:
                realspeed = speed
            movement(mantain, realspeed)
            if counter == 15:
                mouthchange = True
                closed = not closed
                counter = 0
            else:
                counter += 1
            turn = 0

        if not quit:
            if mouthchange:
                if closed:
                    jp.image = closedpac
                else:
                    jp.image = currentpac


            g.update(mazesprites, m.getWidth())
            jp.update(mazesprites, m.getWidth())
            changedir(key, playershadow, jp)
            g.draw(pantalla)

            """
            if key == pygame.K_UP:
                print("up")
            elif key == pygame.K_DOWN:
                print("down")
            if key == pygame.K_LEFT:
                print("left")
            if key == pygame.K_RIGHT:
                print("right")
            print(collision)
            """
            ls = pygame.sprite.spritecollideany(playershadow, mazesprites, False)
            if ls == None and pendingturn:
                mantain = key
                pendingturn = False
                updatemain(jp, mantain)
                if key == pygame.K_RIGHT:
                    currentpac = rightpac
                elif key == pygame.K_LEFT:
                    currentpac = leftpac
                elif key == pygame.K_UP:
                    currentpac = uppac
                elif key == pygame.K_DOWN:
                    currentpac = downpac
            pygame.display.flip()

        pantalla.blit(magic, (DOCK[0] + TILESIZE * (m.getWidth() - 1) , DOCK[1] + 8 * TILESIZE))
        pantalla.blit(magic, (DOCK[0] - TILESIZE , DOCK[1] + 8 * TILESIZE))
        clock.tick(450)
        #print(clock.get_fps())
        turn += 1

        #pos = pygame.mouse.get_pos()
        #print(pos)

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


def movement(key, speed, jp):
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


class Facade(object):
    def handlekeydown(self, event, key, playershadow, jp, collision, mantain, pendingturn):
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

if __name__ == '__main__':
    pygame.init()
    mazelocation = "/home/juan/Escritorio/Project/maze.txt"
    FREE = 200
    bob = Builder(mazelocation, FREE)
    slowturn = 0
    pantalla = bob.buildscreen()
    clock = pygame.time.Clock()
    pantalla.fill(black)
    m = bob.buildmaze()
    m.draw()
    mazesprites = m.getSprites()
    playersize = bob.playersize()
    TILESIZE = bob.tilesize()
    DOCK = bob.dock()

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

    jp = bob.buildplayer(currentpac)
    playershadow = bob.buildplayer(currentpac)
    g = pygame.sprite.GroupSingle()
    g.add(jp)


    quit = collision = pendingturn = mouthchange = closed = habil = False
    speed  = 1
    magic = bob.buildmagic()
    pacdotmagic = bob.builcpacdotmagic()
    pacdotmagic.fill(black)
    magic.fill(black)
    key = None
    turn = counter = 0
    turnspeed = speed * 2

    start = move = True
    mantain = pygame.K_LEFT
    updatemain(jp, mantain)
    pacdots = bob.buildpacdots(m)
    pacdots.draw(pantalla)

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
            if (jp.posx < DOCK[0] + 2 * TILESIZE or jp.posx > DOCK[0] + (m.getWidth() - 4) * TILESIZE) and (jp.posy >= TILESIZE * 10 and jp.posy <= TILESIZE * 11):
                realspeed = speed * 1.5
            elif slowturn != 0:
                pass
            else:
                realspeed = speed
            movement(mantain, realspeed, jp)
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
        paccolide = pygame.sprite.spritecollide(playershadow, pacdots, False)
        if len(paccolide) != 0:
            for o in paccolide:
                pantalla.blit(pacdotmagic, (o.rect.x, o.rect.y))
                o.kill()
            habil = True
        else:
            if slowturn > turnspeed * 5:
                slowturn = 0
                habil = False
        if slowturn != 0:
            realspeed = speed * .3
        else:
            realspeed = speed

        pantalla.blit(magic, (DOCK[0] + TILESIZE * (m.getWidth()) , DOCK[1] + 8 * TILESIZE))
        pantalla.blit(magic, (DOCK[0] - TILESIZE , DOCK[1] + 8 * TILESIZE))


        pygame.display.flip()
        clock.tick(450)

        turn += 1
        if habil:
            slowturn += 1


        #pos = pygame.mouse.get_pos()
        #print(pos)

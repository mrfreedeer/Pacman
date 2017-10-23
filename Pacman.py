import pygame
from maze import *
from pygame.locals import *

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
TILESIZE = 31

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
    playersize = TILESIZE - 1
    startx = DOCK[0] + 3 * TILESIZE
    starty = DOCK[1] + 15 * TILESIZE - 15

    jp = Jugador(playersize,playersize, DOCK, TILESIZE, startx, starty)
    playershadow = Jugador(playersize,playersize, DOCK, TILESIZE, startx, starty)
    g = pygame.sprite.Group()
    g.add(jp)
    ancholab = m.getWidth() + DOCK[0]
    limitancho = ancholab * m.getTile()
    s = 0
    quit = False
    eating = False
    speed  = 2
    magic = pygame.Surface((TILESIZE,TILESIZE))
    magic.fill(black)
    move = False
    key = None
    turn = 0
    turnspeed = 3
    collision = False
    pendingturn = False

    mantain = pygame.K_LEFT
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
            else:
                if pendingturn:
                    mantain = key
                    pendingturn = False
                    print("turnnow")
            if not collision:
                mantain = key
                pendingturn = False
                if mantain == pygame.K_RIGHT:
                    move = True
                    jp.x = 5
                elif mantain == pygame.K_LEFT:
                    move = True
                    jp.x = -5
                elif mantain == pygame.K_UP:
                    move = True
                    jp.y = -5
                elif mantain == pygame.K_DOWN:
                    move = True
                    jp.y = 5
                if mantain == pygame.K_DOWN or mantain == pygame.K_UP:
                    jp.x = 0

                elif mantain == pygame.K_LEFT or mantain == pygame.K_RIGHT:
                    jp.y = 0

        if move and turn >= turnspeed:
            if eating:
                realspeed = speed * .5
            elif (jp.posx < DOCK[0] + 4 * TILESIZE or jp.posx > DOCK[0] + (m.getWidth() - 4) * TILESIZE) and (jp.posy >= TILESIZE * 10 and jp.posy <= TILESIZE * 11):
                realspeed = speed * 2
            else:
                realspeed = speed
            movement(mantain, realspeed)
            turn = 0


        #m.draw(pantalla)
        if not quit:
            g.update(mazesprites, m.getWidth())
            jp.update(mazesprites, m.getWidth())
            changedir(key, playershadow, jp)


            g.draw(pantalla)
            pantalla.blit(magic, (DOCK[0] - 18 + TILESIZE * m.getWidth() , DOCK[1] + 9 * TILESIZE - 10))
            pantalla.blit(magic, (DOCK[0] - TILESIZE , DOCK[1] + 9 * TILESIZE - 10))
            pygame.display.flip()
            if key == pygame.K_UP:
                print("up")
            elif key == pygame.K_DOWN:
                print("down")
            if key == pygame.K_LEFT:
                print("left")
            if key == pygame.K_RIGHT:
                print("right")
            print(collision)



        turn += 1

        #pos = pygame.mouse.get_pos()
        #print(pos)

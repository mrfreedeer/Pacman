import pygame
import math
from maze import *
from pygame.locals import *

red = (255,0,0)         #rgb(255,0,0)
green = (0,255,0)       #rgb(0,255,0)
blue = (0,0,255)        #rgb(0,0,255)
darkBlue = (0,0,128)    #rgb(0,0,128)
yellow =(255,255,51)    #rgb(255,255,51)
white = (255,255,255)   #rgb(255,255,255)
black = (0,0,0)         #rgb(0,0,0)
pink = (255,200,200)    #rgb(255,200,200)


def movement(key, speed, jp):   #Maneja el movimiento del jugador
    if key == pygame.K_RIGHT:   #para actualizarlo en caso de que la
        jp.rect.x += speed      #tecla oprimida cambie
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
def changedir(key, playershadow, jp):   #Reajusta la dirección de la sombra del jugador
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
def updatemain(jp, mantain):        #Ajusta solamente la dirección del movimiento
    if mantain == pygame.K_RIGHT:   #del jugador (arriba, abajp, etc)
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

def die(jp, deathimages, pantalla):
    imageind = 0
    while imageind <= 6:
        pygame.draw.rect(pantalla, black, (jp.posx, jp.posy, playersize, playersize) )
        pantalla.blit(deathimages[imageind],(jp.rect.x, jp.rect.y))
        pygame.display.flip()
        pygame.time.delay(100)
        imageind += 1
if __name__ == '__main__':
    pygame.init()   #Inicializa a Pygame
    pygame.font.init()

    mazelocation = "C://Users//Juan Pablo//Desktop//Pacman//maze.txt"
    FREE = 200
    bob = Builder(mazelocation, FREE)
    slowturn = 0                      #Variable para ralentizar al jugador
    pantalla = bob.buildscreen()      #Construye la pantalla
    clock = pygame.time.Clock()       #Reloj para acelerar el refresco de los gráficos
    pantalla.fill(black)              #Rellena la pantalla de negro
    m = bob.buildmaze()               #Construye el laberinto dejando un espacio
                                      #libre en la pantalla (FREE)
    m.draw()                          #Dibuja el laberinto
    mazesprites = m.getSprites()      #Obtiene los Sprites del laberinto:
                                      #Paredes, y lineas para interactuar
                                      #Con ellas (colisiones)
    playersize = bob.playersize()
    TILESIZE = bob.tilesize()
    DOCK = bob.dock()
    font = pygame.font.Font('emulogic.ttf',int(bob.tilesize()/2) )
    pausefont = pygame.font.Font('emulogic.ttf', int(bob.tilesize()))
    scoreposy = DOCK[1] + (m._height * TILESIZE) + 10

    #Manejo de las imagenes de Pacman
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

    string = 'Pdying'
    png = '.png'
    deathimages = []
    for h in range(1,8):
        image = pygame.image.load(string+str(h)+png).convert_alpha()
        deathimages.append(pygame.transform.scale(image,(playersize,playersize)))


    jp = bob.buildplayer(currentpac)
    playershadow = bob.buildplayer(currentpac)

    #Para dibujar un Sprite, se añade a un grupo de Sprites primer
    #El grupo puede tener un solo elemento (GroupSingle) o muchos
    #(Group)
    g = pygame.sprite.GroupSingle()
    g.add(jp)


    quit = collision = pendingturn = mouthchange = closed = start = move = habil = False
    speed  = 1
    magic = bob.buildmagic()
    pacdotmagic = bob.builcpacdotmagic()
    pacdotmagic.fill(black)
    magic.fill(black)
    key = None
    turn = counter = 0
    turnspeed = speed * 2

    mantain = pygame.K_LEFT
    updatemain(jp, mantain)
    pacdots = bob.buildpacdots(m)
    score = bob.buildscore()
    pacdots.draw(pantalla)
    scbase = font.render("Score", True, (255,255,255))
    pantalla.blit(scbase, (DOCK[0],scoreposy))
    scorepts = font.render("0", True, (255,255,255))
    currentscore = prevscore = score.getScore()
    scoreposx = scbase.get_width() + DOCK[0] + 10
    pantalla.blit(scorepts, (scoreposx, scoreposy))
    pause = pauseStart = False
    pausepac = pygame.sprite.Group()
    pausetxt = pausefont.render("Pause", True, white)
    redraweverything = False
    pausepos = (DOCK[0] + 6 * TILESIZE, DOCK[1] + 9 * TILESIZE)
    readytxt = font.render("READY!", True,yellow)
    time = 0
    timestart = True
    timefinish = False
    pantalla.blit(pygame.Surface((TILESIZE * 4, TILESIZE)),(pausepos[0] + TILESIZE , pausepos[1] + 2 * TILESIZE))
    pantalla.blit(readytxt, (pausepos[0] + TILESIZE , pausepos[1] + 2 * TILESIZE))

    while True:
        '''
        if score._dotnum == 0:
            move = False
            die(jp, deathimages, pantalla)
        '''
        if time < 3000 and timestart:
            pygame.time.delay(10)
            time += 10
        else:
            if not move:
                timestart = False
                timefinish = True
        if timefinish:
            start = move = True
            timefinish = False
            redraweverything = True

        if pause:
            if pauseStart:
                pygame.draw.rect(pantalla, black, (jp.posx, jp.posy, playersize, playersize) )
                pausepacplayer = bob.buildplayer(closedpac, jp.rect.x, jp.rect.y)
                pausepac = pygame.sprite.Group()
                pausepac.add(pausepacplayer)
                pauseStart = False
                pausepac.draw(pantalla)
                pantalla.blit(pausetxt, pausepos)
                redraweverything = True
                pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    quit = True

                #Maneja cuando opriman un botón
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False

        else:
            if redraweverything:
                pantalla.fill(black)
                m.draw()
                pacdots.draw(pantalla)
                g.draw(pantalla)
                pantalla.blit(scbase, (DOCK[0],scoreposy))
                pantalla.blit(scorepts, (scoreposx, scoreposy))
                DOCK[0] + 8 * TILESIZE, DOCK[1] + 8 * TILESIZE
                pantalla.blit(pygame.Surface((5, m._height * TILESIZE)),(DOCK[0] - TILESIZE - 5, DOCK[1]))
                pantalla.blit(pygame.Surface((5, m._height * TILESIZE)),(DOCK[0] + TILESIZE * (m._width + 1) + 5, DOCK[1]))
                pantalla.blit(pygame.Surface((TILESIZE, 1)),(DOCK[0] + 8 * TILESIZE, DOCK[1] + 8 * TILESIZE))
                redraweverything = False


            #Dibuja un Rectangulo Negro encima del jugador para luego
            #Redibujarlo en otra posición
            pygame.draw.rect(pantalla, black, (jp.posx, jp.posy, playersize, playersize) )

            #Maneja los eventos de teclado y ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    quit = True

                #Maneja cuando opriman un botón
                if event.type == pygame.KEYDOWN:
                    if event.key != pygame.K_p:
                        key = event.key
                    changedir(key, playershadow, jp)
                    collision = False
                    if event.key == pygame.K_p:
                        pause = pauseStart = True

                    #Esta función (spritecollideany) retorna None cuando no hay
                    #colisiones, y un Sprite cuando Sí

                    ls = pygame.sprite.spritecollideany(playershadow, mazesprites, False)
                    if ls != None:
                        collision = True
                        if mantain != key:
                            pendingturn = True

                    #Los movimientos son sostenidos
                    #Es decir, se mantienen hasta que se cambie de movimiento
                    #En tal caso, cambia de movimiento en cuanto sea posible
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


            #Manejo de movimiento de Pacman
            #Se mueve después de un número de turnos, para que
            #el movimiento no sea demasiado rápido

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

                #Se actualizan los grupos de Sprite y los Sprite
                #para actualizar la posicion de los Sprites en la
                #pantalla y redibujarlos
                g.update(mazesprites, m.getWidth())
                jp.update(mazesprites, m.getWidth())
                changedir(key, playershadow, jp)

                #Se dibuja a Pacman
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

                #Se encarga de cambiar de dirección en caso de
                #que exista un movimiento pendiente
                #que no se había podido realizar
                #debido a colisiones con el laberinto
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

            #Colisiones con los pacdots
            #En caso de colisionar con éstos,
            #Pacman se mueve más lento
            paccolide = pygame.sprite.spritecollide(playershadow, pacdots, False)
            if len(paccolide) != 0:
                for o in paccolide:
                    pantalla.blit(pacdotmagic, (o.rect.x, o.rect.y))
                    o.kill()
                    score.consume()
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
            currentscore = score.getScore()
            if prevscore != currentscore:
                scorepts = font.render(str(currentscore), True, white)
                prevscore = currentscore
                scoremagic = pygame.Surface((TILESIZE * 5, TILESIZE))
                pantalla.blit(scoremagic, (scoreposx,scoreposy))
                pantalla.blit(scorepts, (scoreposx, scoreposy))
            turn += 1
            if habil:
                slowturn += 1


        #pos = pygame.mouse.get_pos()
        #print(pos)

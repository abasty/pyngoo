# This module defines the play state

import random
import pygame
import game

#font = pygame.font.Font(None, 50)

back = pygame.image.load("media/playbackground.png").convert()
glacon = pygame.image.load("media/glacon.png").convert()
glacon.set_colorkey(glacon.get_at((0,0)), pygame.RLEACCEL)
bord = pygame.image.load("media/igloo.jpg").convert()
neige = pygame.image.load("media/neige.jpg").convert()
tux = pygame.image.load("media/tux.png").convert_alpha()


# Move should be computed on time (see clock) because tick is not stable
blocksize = 40
moveframes = 8
movesize = int(blocksize / moveframes)
motionticktime = int(100 / moveframes)
ticknumber = 0

lmax = 13
cmax = 19
lorigin = 60
corigin = 20

player = game.Object()

# Initialization
def init():
    pass

def enter():
    # Player
    global player
    player.lig = int(lmax / 2)
    player.col = int(cmax / 2)
    player.dlig = 0
    player.dcol = 0
    player.x = player.col * blocksize + corigin
    player.y = player.lig * blocksize + lorigin
    player.key = -1
    player.picture = tux

    # Labyrinth
    global tableau
    tableau = []
    ligne0 = [ "b" ] * cmax
    tableau.append(ligne0)
    for l in range(lmax / 2):
        ligne0 = [ "b" ]
        ligne1 = [ "b" ]
        for c in range(cmax / 2):
            r = random.choice(["xx..", "xx..", "x.x.", "x.x.", "x..."])
            if c > 0:
                ligne0.append(r[0])
                ligne1.append(r[2])
            ligne0.append(r[1])
            ligne1.append(r[3])
        ligne0.append("b")
        ligne1.append("b")
        if l > 0:
            tableau.append(ligne0)
        tableau.append(ligne1)
    ligne0 = [ "b" ] * cmax
    tableau.append(ligne0)
    tableau[player.lig][player.col] = "."

    pygame.time.set_timer(game.MOTIONTICK, motionticktime)

def leave():
    pygame.time.set_timer(game.MOTIONTICK, 0)
    pass

def define_move(key):
    player.key = key

def undefine_move_if_equal(key):
    pass
#    if player.key == key:
#        player.key = -1

def begin_move():
    # end move
    player.col += player.dcol
    player.lig += player.dlig
    player.dcol = 0
    player.dlig = 0
    player.dx = 0
    player.dy = 0

    if player.key == pygame.K_UP:
        dcol = 0
        dlig = -1
    elif player.key == pygame.K_DOWN:
        dcol = 0
        dlig = 1
    elif player.key == pygame.K_LEFT:
        dcol = -1
        dlig = 0
    elif player.key == pygame.K_RIGHT:
        dcol = 1
        dlig = 0
    else:
        dcol = 0
        dlig = 0

    collision = tableau[player.lig + dlig][player.col + dcol]
    
    if collision == ".":
        player.dcol = dcol
        player.dlig = dlig
        player.dx = dcol * movesize
        player.dy = dlig * movesize

def move():
    player.x += player.dx
    player.y += player.dy

def motiontick():
    global ticknumber
    if ticknumber == 0:
        begin_move()
    move()

    ticknumber = (ticknumber + 1) % moveframes

# Event callback
def event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "Menu"
        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            # try w/ sets (event.key in (...)
            define_move(event.key)
        return
    
#    if event.type == pygame.KEYUP:
#        undefine_move_if_equal(event.key)
 #       return

    if event.type == game.MOTIONTICK:
        motiontick()

# Draw callback
def draw():
    game.screen.blit(back, [0, 0])

    # draw board
    y = lorigin
    for l in range(len(tableau)):
        ligne = tableau[l]
        x = corigin
        for c in range(len(ligne)):
            item = ligne[c]
            if item == "x":
                game.screen.blit(glacon, [ x, y ])
            elif item == "b":
                game.screen.blit(bord, [ x, y ])
            x += blocksize
        y += blocksize

    # draw player
    game.screen.blit(player.picture, [ player.x, player.y ])

init()

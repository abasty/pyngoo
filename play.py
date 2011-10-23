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
    player.picture = tux

    # Labyrinth
    global tableau
    tableau = []
    ligne0 = [ "b" for _ in range(cmax) ]
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
    ligne0 = [ "b" for _ in range(cmax) ]
    tableau.append(ligne0)
    tableau[player.lig][player.col] = "."

    pygame.time.set_timer(game.MOTIONTICK, motionticktime)

def leave():
    pygame.time.set_timer(game.MOTIONTICK, 0)
    pass

def begin_move(dcol, dlig):
    collision = tableau[player.lig + dlig][player.col + dcol]
    if collision == ".":
        player.dcol = dcol
        player.dlig = dlig
        player.dx = dcol * movesize
        player.dy = dlig * movesize

def end_move():
    player.col += player.dcol
    player.lig += player.dlig
    player.dcol = 0
    player.dlig = 0
    player.dx = 0
    player.dy = 0
    
def move():
    player.x += player.dx
    player.y += player.dy

def motiontick():
    global ticknumber
    if ticknumber == 0:
        end_move()
        kb = pygame.key.get_pressed()
        if kb[pygame.K_UP]:
            begin_move(0, -1)
        elif kb[pygame.K_DOWN]:
            begin_move(0, +1)
        elif kb[pygame.K_LEFT]:
            begin_move(-1, 0)
        elif kb[pygame.K_RIGHT]:
            begin_move(+1, 0)
        else:
            begin_move(0, 0)
    move()
        
    ticknumber = (ticknumber + 1) % moveframes
    
# Event callback
def event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "Menu"
        return

    if event.type == pygame.MOUSEBUTTONDOWN:
        return "Menu"

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

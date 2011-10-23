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

spriteSize = 40
lmax = 13
cmax = 19
lorigin = 60
corigin = 20

player = game.Object()
player.x = int(cmax / 2)
player.y = int(lmax / 2)
player.picture = tux

# Initialization
def init():
    pass

def enter():
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
    tableau[ player.y ] [ player.x ] = "."

    pygame.time.set_timer(game.TICK, 100)

def leave():
    pygame.time.set_timer(game.TICK, 0)

def move_player(dx, dy):
    collision = tableau[player.y + dy][player.x + dx]
    if collision == ".":
        player.x += dx
        player.y += dy

def tick():
    kb = pygame.key.get_pressed()
    if kb[pygame.K_UP]:
        move_player(0, -1)
    elif kb[pygame.K_DOWN]:
        move_player(0, +1)
    elif kb[pygame.K_LEFT]:
        move_player(-1, 0)
    elif kb[pygame.K_RIGHT]:
        move_player(+1, 0)

# Event callback
def event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "Menu"
        return

    if event.type == pygame.MOUSEBUTTONDOWN:
        return "Menu"

    if event.type == game.TICK:
        tick()

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
            x += spriteSize
        y += spriteSize
        
    # draw player
    game.screen.blit(player.picture, [ player.x * spriteSize + corigin, player.y *spriteSize + lorigin])

init()

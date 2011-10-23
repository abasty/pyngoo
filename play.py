# This module defines the play state

import random
import pygame
import game

title = "Play"
font = pygame.font.Font(None, 50)
back = pygame.image.load("media/playbackground.png").convert()
glacon = pygame.image.load("media/glacon.png").convert()
glacon.set_colorkey(glacon.get_at((0,0)), pygame.RLEACCEL)
bord = pygame.image.load("media/igloo.jpg").convert()
neige = pygame.image.load("media/neige.jpg").convert()
tableau = []

spriteSize = 40
lmax = 13
cmax = 19
lorigin = 60
corigin = 20

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

# Event callback
def event(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return "Menu"
    if event.type == pygame.MOUSEBUTTONDOWN:
        return "Menu"

# Draw callback
def draw():
    game.screen.blit(back, [0, 0])

    for l in range(len(tableau)):
        ligne = tableau[l]
        for c in range(len(ligne)):
            item = ligne[c]
            if item == "x":
                game.screen.blit(glacon, [c * spriteSize + corigin, l * spriteSize + lorigin ])
            elif item == "b":
                game.screen.blit(bord, [c * spriteSize + corigin, l * spriteSize + lorigin ])

init()

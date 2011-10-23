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

spriteSize = 42
lmax = 12
cmax = 14

# Initialization
def init():
    pass

def enter():
    # Labyrinth
    global tableau
    tableau = []
    ligne0 = [ "b" for _ in range(cmax + 2) ]
    tableau.append(ligne0)
    for _ in range(lmax / 2):
        ligne0 = [ "b" ]
        ligne1 = [ "b" ]
        for _ in range(cmax / 2):
            r = random.choice(["xx..", "xx..", "x.x.", "x.x.", "x..."])
            ligne0.append(r[0])
            ligne0.append(r[1])
            ligne1.append(r[2])
            ligne1.append(r[3])
        ligne0.append("b")
        ligne1.append("b")
        tableau.append(ligne0)
        tableau.append(ligne1)
    ligne0 = [ "b" for _ in range(cmax + 2) ]
    tableau.append(ligne0)

# Event callback
def event(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return "Menu"
    if event.type == pygame.MOUSEBUTTONDOWN:
        return "Menu"

# Draw callback
def draw():
#    game.screen.fill(0xb4b4d9)
    game.screen.blit(back, [0, 0])
    game.screen.blit(font.render(title, True, [0, 0, 0]), [0, 0])

    for l in range(len(tableau)):
        ligne = tableau[l]
        for c in range(len(ligne)):
            item = ligne[c]
            if item == "x":
                game.screen.blit(glacon, [c * spriteSize + 20 + 90, l * spriteSize ])
            elif item == ".":
                #game.screen.blit(neige, [c * spriteSize + 20 + 90, l * spriteSize ])
                #pygame.draw.rect(game.screen, 0x808080, pygame.Rect(c * spriteSize + 20 + 90, l * spriteSize, spriteSize, spriteSize))
                pass
            elif item == "b":
                game.screen.blit(bord, [c * spriteSize + 20 + 90, l * spriteSize ])
                #pygame.draw.rect(game.screen, game.gray, pygame.Rect(c * spriteSize + 20 + 90, l * spriteSize, spriteSize, spriteSize))

init()

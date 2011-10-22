# This module defines the play state

import random
import pygame
import game

title = "Play"
font = pygame.font.Font(None, 50)
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
    ligne0 = [ "b" for i in range(cmax + 2) ]
    tableau.append(ligne0)
    for l in range(lmax / 2):
        ligne0 = [ "b" ]
        ligne1 = [ "b" ]
        for c in range(cmax / 2):
            r = random.choice(["xx..", "xx..", "x.x.", "x.x.", "x..."])
            ligne0.append(r[0])
            ligne0.append(r[1])
            ligne1.append(r[2])
            ligne1.append(r[3])
        ligne0.append("b")
        ligne1.append("b")
        tableau.append(ligne0)
        tableau.append(ligne1)
    ligne0 = [ "b" for i in range(cmax + 2) ]
    tableau.append(ligne0)

# Event callback
def event(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return "Menu"
    if event.type == pygame.MOUSEBUTTONDOWN:
        return "Menu"

# Draw callback
def draw():
    game.screen.fill(game.white)
    game.screen.blit(font.render(title, True, [0, 0, 0]), [0, 0])

    for l in range(len(tableau)):
        ligne = tableau[l]
        for c in range(len(ligne)):
            item = ligne[c]
            if item == "x":
                pygame.draw.rect(game.screen, 0, pygame.Rect(c * spriteSize + 20 + 90, l * spriteSize, spriteSize, spriteSize), 4)
            elif item == "b":
                pygame.draw.rect(game.screen, game.gray, pygame.Rect(c * spriteSize + 20 + 90, l * spriteSize, spriteSize, spriteSize))

init()

# This module defines the play state

import random
import pygame
import game

title = "Play"
font = pygame.font.Font(None, 50)
tableau = []
spriteSize = 30

# Initialization
def init():
    pass

def enter():
    # Labyrinth
    global tableau
    tableau = []
    for l in range(10):
        ligne0 = []
        ligne1 = []
        for c in range(12):
            r = random.choice(["xx..", "xx..", "x.x.", "x.x.", "x..."])
            ligne0.append(r[0])
            ligne0.append(r[1])
            ligne1.append(r[2])
            ligne1.append(r[3])
        tableau.append(ligne0)
        tableau.append(ligne1)

# Event callback
def event(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return "Menu"
    if event.type == pygame.MOUSEBUTTONDOWN:
        return "Menu"

# Draw callback
def draw():
    game.screen.fill([255, 0, 255])
    game.screen.blit(font.render(title, True, [0, 0, 0]), [0, 0])

    for l in range(len(tableau)):
        ligne = tableau[l]
        for c in range(len(ligne)):
            item = ligne[c]
            if item == "x":
                pygame.draw.rect(game.screen, 0, pygame.Rect(c * spriteSize + 20 + 90, l * spriteSize, spriteSize, spriteSize))

init()

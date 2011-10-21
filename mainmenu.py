# This module defines the mainmenu state

import pygame
import game

# Global Declarations
menu = [ "Play", "Setup", "About", " ", "Quit" ]
zones = [ ]
renderedText = [ ]
selected = -1

# Initialization
def init():
    fontSize = 100
    font = pygame.font.Font(None, fontSize)
    maxWidth = 0
    for item in menu:
        renderedText.append(font.render(item, True, [0, 0, 0]))
        extents = font.size(item)
        if extents[0] > maxWidth:
            maxWidth = extents[0]
    
    X = (game.size[0] - maxWidth) / 2;
    Y = (game.size[1] - len(menu) * fontSize) / 2;
    for item in menu:
        zones.append(pygame.Rect(X, Y, maxWidth, fontSize))
        Y += fontSize

# Event callback
def event(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return "Quit"
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        for i in range(len(zones)):
            if zones[i].collidepoint(event.pos):
                return menu[i]

# Draw callback
def draw():
    game.screen.fill([255, 255, 255])
    for i in range(len(renderedText)):
        game.screen.blit(renderedText[i], zones[i].topleft)


init()

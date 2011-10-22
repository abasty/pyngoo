# This module defines the mainmenu state

import pygame
import game

# Global Declarations
menu = [ "Play", "Setup", "About", "Quit" ]
zones = [ ]
renderedText = [ ]
selected = -1
fontSize = 100

# Initialization
def init():
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

def enter():
    pass

# Event callback
def event(event):
    global selected
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "Quit"
        elif event.key == pygame.K_RETURN:
            if selected == -1:
                return "Play"
            else:
                return menu[selected]
        elif event.key == pygame.K_DOWN:
            selected = (selected + 1) % len(menu)
        elif event.key == pygame.K_UP:
            selected = (selected + len(menu) - 1) % len(menu)
        return

    if event.type == pygame.MOUSEBUTTONDOWN:
        for i in range(len(zones)):
            if zones[i].collidepoint(event.pos):
                return menu[i]
        return

    if event.type == pygame.MOUSEMOTION:
        selected = -1
        for i in range(len(zones)):
            if zones[i].collidepoint(event.pos):
                selected = i
        return

# Draw callback
def draw():
    game.screen.fill(0xb4b4d9)
    if selected != -1:
        r = zones[selected].copy()
        r.left = 20
        r.width = game.size[0] - 2 * r.left
        r.top -= r.height / 4
        pygame.draw.rect(game.screen, 0xffffff, r, 4)
        r.inflate(-4, -4)
        pygame.draw.rect(game.screen, 0x5b5ba0, r)
    for i in range(len(renderedText)):
        game.screen.blit(renderedText[i], zones[i].topleft)

init()

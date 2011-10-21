# This module defines the play state
import pygame
import game

title = "Setup"
font = pygame.font.Font(None, 50) 

# Initialization
def init():
    pass

# Event callback
def event(event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return "Menu"

# Draw callback
def draw():
    game.screen.fill([255, 0, 255])
    game.screen.blit(font.render(title, True, [0, 0, 0]), [0, 0])
    
init()

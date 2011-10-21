# This module defines the play state
import pygame
import game

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

init()

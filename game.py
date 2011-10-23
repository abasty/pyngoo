import pygame

# Define the colors we will use in RGB format
black = [  0,  0,  0]
white = [255,255,255]
blue =  [  0,  0,255]
green = [  0,255,  0]
red =   [255,  0,  0]
gray =  [127, 127, 127]

pi = 3.141592653

# Set the height and width of the game.screen
size = [ 800, 600 ]

#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyGame Example - Alain Basty")

TICK = pygame.USEREVENT

class Object:
    pass

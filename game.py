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

# Decal on play screen
xorigin = 20
yorigin = 60

DIRECTION_NONE = 0
DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4

#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyGame Example - Alain Basty")

TRANSPARENCY_COLORKEY_AUTO = -1
TRANSPARENCY_ALPHA = -2
TRANSPARENCY_NONE = None

# input
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

inputMode = INPUT_KEYBOARD

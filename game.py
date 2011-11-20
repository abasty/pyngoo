import os
import pygame
from pygame.locals import RLEACCEL

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

#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyGame Example - Alain Basty")

MOTIONTICK = pygame.USEREVENT

def load_image(name, colorkey=None):
    fullname = os.path.join('media', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Object:
    pass

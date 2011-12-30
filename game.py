import os
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

# FIXME: Implement image cache = create an associative array between image name and image itself
# FIXME: Do not load the image if the image is already available in the cache

def load_image(name, colorkey, n = 1):
    fullname = os.path.join('media', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if colorkey is TRANSPARENCY_ALPHA:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey is not None:
            if colorkey is TRANSPARENCY_COLORKEY_AUTO:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

    r = image.get_rect()
    r.w = r.w / n

    return image, r

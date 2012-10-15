import pygame
import os

# Define the colors we will use in RGB format
white = [255,255,255]

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

_image_cache = { }

def load_image(name, colorkey):
    fullname = os.path.join('media', name)

    image = _image_cache.get(fullname)
    if image:
        return image

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

    _image_cache[fullname] = image

    return image

def destroy_image_cache():
    _image_cache = { }

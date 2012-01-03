import os
import math
import pygame
from game import *

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

class Vector2d:
    """A class to manipulate 2d vectors such as position or speed"""
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2d(self.x - other.x, self.y - other.y)

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def copy(self):
        return Vector2d(self.x, self.y)

    def length(self):
        if self.x == 0:
            return abs(self.y)
        elif self.y == 0:
            return abs(self.x)
        else:
            return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self, r = 1.0):
        l = self.length()
        return Vector2d(self.x / l * r, self.y / l * r)

class Physics:

    t = 0
    dt = 20
    
    @classmethod
    def pixelsPerSecondToSpeedUnit(self, pxBysec):
        return pxBysec * self.dt / 1000.0

class PhysicsSprite(pygame.sprite.DirtySprite):
    """An object that implements simple 2d physics"""
    STATE_NORMAL = 0

    def __init__(self, l, c, image, colorkey, n, velocityMaxInPixelsPerSeconds):
        """
        Initialize a new PhysicsObject instance
        
        l -- pseudo line (vertical coordinate) of the object
        c -- pseudo column (horizontal coordinate) of the object
        image -- name of an image file in the medi folder
        colorkey -- color key of the image (can be None, ALPHA, COLORKEY_AUTO)
        n -- How many sprite frames in the image file
        velocityMaxInPixelsPerSeconds -- Maximum velocity of the object
        """
        pygame.sprite.DirtySprite.__init__(self)
        self.image, self.rect = load_image(image, colorkey, n)
        self.source_rect = self.rect.copy()
        self.position = Vector2d(xorigin + c * self.rect.w, yorigin + l * self.rect.h)
        self.rect.move_ip(self.position.x, self.position.y)
        self.target = self.position.copy()
        self.velocity = Vector2d(0.0, 0.0)
        self.velocityMax = Physics.pixelsPerSecondToSpeedUnit(velocityMaxInPixelsPerSeconds)
        self.direction = DIRECTION_NONE
        self.lastRect = self.rect
        self.state = self.STATE_NORMAL

    def updateTarget(self):
        """This method computes new target given AI or key input
        It should be overridden in subclasses"""
        pass

    def setAnimationFrame(self, n):
        self.currentFrame = n
        self.source_rect.left = n * self.source_rect.w
        self.dirty = 1

    def startAnimation(self, t, frames, frameRate, loopAnimation = False):
        self.frames = frames
        self.framesCount = len(self.frames)
        self.currentIndex = 0
        self.nextFrameT = t
        self.deltaFrameT = 1000.0 / frameRate
        self.loopAnimation = loopAnimation

    def updateAnimation(self, t):
        if self.currentIndex < 0:
            return
        while t > self.nextFrameT:
            self.nextFrameT += self.deltaFrameT
            self.currentIndex += 1
        if self.currentIndex < self.framesCount:
            self.setAnimationFrame(self.frames[self.currentIndex])
        elif self.loopAnimation:
            self.currentIndex = 0
            self.setAnimationFrame(self.frames[0])
        else:
            self.currentIndex = -1
        self.dirty = 1

    def updatePhysics(self):
        # get target if needed
        if self.position == self.target:
            self.updateTarget()
        # compute delta to target and velocity to apply
        # NOTE: this is a simple physics algo w/ only velocity applied to position
        # NOTE: More complex physics can be implemented here based on ramp
        # NOTE: acceleration, or other imagined physics.
        delta = self.target - self.position
        # shortcut to null movement
        if delta == Vector2d(0, 0):
            return

        # max speed control
        if delta.length() <= self.velocityMax:
            self.velocity = delta
        else:
            self.velocity = delta.normalize(self.velocityMax)
        # apply velocity
        self.position += self.velocity

        # apply physics to pygame sprite (and recall last position to enable cancel)
        self.lastRect = pygame.Rect(self.rect)
        self.rect.left = self.position.x
        self.rect.top = self.position.y
        self.dirty = 1        

    def cancelPhysics(self):
        self.rect = self.lastRect
        self.position = Vector2d(self.lastRect.x, self.lastRect.y)
        self.target = Vector2d(self.lastRect.x, self.lastRect.y)
        self.direction = DIRECTION_NONE

    def setState(self, state):
        self.state = state

    def push(self, direction):
        """This method is called when the object is pushed in a direction
        It should be overridden in subclasses if the object can be pushed"""
        pass


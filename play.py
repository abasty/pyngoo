# This module defines the play state

import random
import pygame
import math
from game import screen, load_image, xorigin, yorigin, ALPHA, COLORKEY_AUTO

back = pygame.image.load("media/playbackground.png").convert()

lmax = 13
cmax = 19

nextT = 0
deltaT = 20

DIRECTION_NONE = 0
DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4

def pixelsBySecondToSpeedUnit(pxBysec):
    return pxBysec * deltaT / 1000.0

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

class PhysicsSprite(pygame.sprite.Sprite):
    """An object that implements simple 2d physics"""
    def __init__(self, position = Vector2d(0.0, 0.0)):
        self.position = position
        self.target = Vector2d(position.x, position.y)
        self.velocity = Vector2d(0.0, 0.0)
        self.velocityMax = 1.0
        self.direction = DIRECTION_NONE

    def updateTarget(self):
        """This method computes new target given AI or key input
        It should be overridden in subclasses"""
        pass

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

    def cancelPhysics(self):
        self.rect = self.lastRect
        self.position = Vector2d(self.lastRect.x, self.lastRect.y)
        self.target = Vector2d(self.lastRect.x, self.lastRect.y)

    def push(self, direction):
        """This method is called when the object is pushed in a direction
        It should be overridden in subclasses if the object can be pushed"""
        pass
    
class Block(PhysicsSprite):
    """The class to represent a block"""
    def __init__(self, l, c):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('glacon.png', COLORKEY_AUTO)
        self.rect.move_ip(xorigin + c * self.rect.w, yorigin + l * self.rect.h)
        PhysicsSprite.__init__(self, Vector2d(self.rect.left, self.rect.top))
        self.velocityMax = pixelsBySecondToSpeedUnit(500.0)

    def updateTarget(self):
        if self.direction == DIRECTION_NONE:
            return
        elif self.direction == DIRECTION_UP:
            self.target.y -= self.rect.h
        elif self.direction == DIRECTION_DOWN:
            self.target.y += self.rect.h
        elif self.direction == DIRECTION_LEFT:
            self.target.x -= self.rect.w
        elif self.direction == DIRECTION_RIGHT:
            self.target.x += self.rect.w

    def update(self):
        self.updatePhysics()
        hit = pygame.sprite.spritecollide(self, labyrinth, False)
        for h in hit:
            if h != self:
                self.cancelPhysics()
                self.direction = DIRECTION_NONE

    def push(self, direction):
        self.direction = direction

class Border(PhysicsSprite):
    """The class to represent a border block"""
    def __init__(self, l, c):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('igloo.jpg')
        self.rect.move_ip(xorigin + c * self.rect.w, yorigin + l * self.rect.h)
    
    def update(self):
        pass

class Pingoo(PhysicsSprite):
    """The pingoo/player class"""
    def __init__(self, l, c):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('tux.png', ALPHA)
        self.rect.move_ip(xorigin + c * self.rect.w, yorigin + l * self.rect.h)
        PhysicsSprite.__init__(self, Vector2d(self.rect.left, self.rect.top))
        self.velocityMax = pixelsBySecondToSpeedUnit(250.0)
        self.pushing = False

    def updateTarget(self):
        # TODO: use something like int(self.target.y / self.rect.h + 1) * self.rect.h
        # TODO: a method like PhysicsSprite.setTargetFromPositionDirection()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.target.y -= self.rect.h
            self.direction = DIRECTION_UP
        elif keys[pygame.K_DOWN]:
            self.target.y += self.rect.h
            self.direction = DIRECTION_DOWN
        elif keys[pygame.K_LEFT]:
            self.target.x -= self.rect.w
            self.direction = DIRECTION_LEFT
        elif keys[pygame.K_RIGHT]:
            self.target.x += self.rect.w
            self.direction = DIRECTION_RIGHT
        else:
            self.target = Vector2d(self.position.x, self.position.y)
            self.direction = DIRECTION_NONE
        
        self.pushing = keys[pygame.K_SPACE]

    def update(self):
        self.updatePhysics()
        hit = pygame.sprite.spritecollide(self, labyrinth, False)
        if hit:
            self.cancelPhysics()
            if self.pushing:
                hit[0].push(self.direction)

# Initialization
def init():
    pass

def enter():
    global labyrinth, player, pingoo
    labyrinth = pygame.sprite.RenderPlain()
    pingoo = Pingoo(lmax / 2, cmax / 2)
    player = pygame.sprite.RenderPlain(pingoo)

    # Labyrinth
    tableau = []
    ligne0 = [ "b" ] * cmax
    tableau.append(ligne0)
    for l in range(lmax / 2):
        ligne0 = [ "b" ]
        ligne1 = [ "b" ]
        for c in range(cmax / 2):
            r = random.choice(["xx..", "xx..", "x.x.", "x.x.", "x..."])
            if c > 0:
                ligne0.append(r[0])
                ligne1.append(r[2])
            ligne0.append(r[1])
            ligne1.append(r[3])
        ligne0.append("b")
        ligne1.append("b")
        if l > 0:
            tableau.append(ligne0)
        tableau.append(ligne1)
    ligne0 = [ "b" ] * cmax
    tableau.append(ligne0)
    tableau[lmax / 2][cmax / 2] = "."

    #define sprites
    for l in range(lmax):
        for c in range(cmax):
            p = tableau[l][c]
            if p is "b":
                labyrinth.add(Border(l, c))
            if p is "x":
                labyrinth.add(Block(l, c))

    global nextT, deltaT
    nextT = pygame.time.get_ticks() + deltaT

def leave():
    global labyrinth, player, pingoo
    labyrinth.empty()
    player.empty()
    del pingoo

# Event callback
def event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "Menu"
        return

# Draw callback
def draw():
    global nextT, deltaT
    t = pygame.time.get_ticks()
    while t >= nextT:
        player.update()
        labyrinth.update()
        nextT += deltaT
    screen.blit(back, [0, 0])
    labyrinth.draw(screen)
    player.draw(screen)

init()

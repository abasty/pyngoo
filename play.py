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

class PhysicsObject:
    """An object that implements simple 2d physics"""
    def __init__(self, position = Vector2d(0.0, 0.0), velocity = Vector2d(0.0, 0.0)):
        self.position = position
        self.target = Vector2d(position.x, position.y)
        self.velocity = velocity
        self.velocityMax = 0.0

    def updateTarget(self):
        """This method computes new target given AI or key input
        It should be overridden in subclasses"""
        pass

    def updatePhysics(self):
        # get target if needed
        if self.position == self.target:
            self.updateTarget()
        # compute delta to target and velocity to apply
        delta = self.target - self.position
        if delta == Vector2d(0, 0):
            return
        if delta.length() <= self.velocityMax:
            self.velocity = delta
        else:
            self.velocity = delta.normalize(self.velocityMax)
        # apply velocity
        self.position += self.velocity

class Block(pygame.sprite.Sprite, PhysicsObject):
    """The class to represent a block"""
    def __init__(self, l, c):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('glacon.png', COLORKEY_AUTO)
        self.rect.move_ip(xorigin + c * self.rect.w, yorigin + l * self.rect.h)
        PhysicsObject.__init__(self, Vector2d(self.rect.left, self.rect.top))

    def update(self):
        pass

class Border(pygame.sprite.Sprite):
    """The class to represent a border block"""
    def __init__(self, l, c):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('igloo.jpg')
        self.rect.move_ip(xorigin + c * self.rect.w, yorigin + l * self.rect.h)
    
    def update(self):
        pass

class Pingoo(pygame.sprite.Sprite, PhysicsObject):
    """The pingoo/player class"""
    def __init__(self, l, c):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('tux.png', ALPHA)
        self.rect.move_ip(xorigin + c * self.rect.w, yorigin + l * self.rect.h)
        PhysicsObject.__init__(self, Vector2d(self.rect.left, self.rect.top))
        self.key = 0
        self.velocityMax = pixelsBySecondToSpeedUnit(100.0)
        self.stop = self.rect.left % self.rect.w

    def updateTarget(self):
        if self.key == pygame.K_UP:
            self.target.y -= self.rect.h
        elif self.key == pygame.K_DOWN:
            self.target.y += self.rect.h
        elif self.key == pygame.K_LEFT:
            self.target.x -= self.rect.w
        elif self.key == pygame.K_RIGHT:
            self.target.x += self.rect.w

    def update(self):
        self.updatePhysics()
        self.rect.left = self.position.x
        self.rect.top = self.position.y

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

def begin_move():
    pass

def move():
    pass

# Event callback
def event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "Menu"
        elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            pingoo.key = event.key
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

# This module defines the play state

import random
import pygame
from game import screen, load_image, xorigin, yorigin, ALPHA, COLORKEY_AUTO

back = pygame.image.load("media/playbackground.png").convert()

lmax = 13
cmax = 19

nextT = 0
deltaT = 20

def pixelsBySecondToSpeedUnit(pxBysec):
    return pxBysec * deltaT / 1000.0

class PhysicsObject:

    def __init__(self, vx = 0.0, vy = 0.0):
        # position
        self.x = self.rect.left
        self.y = self.rect.left
        # speed in pixels/ms
        self.vx = vx
        self.vy = vy

    def doPhysics(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.left = self.x

class Block(pygame.sprite.Sprite, PhysicsObject):

    def __init__(self, l, c):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('glacon.png', COLORKEY_AUTO)
        self.rect.move_ip(xorigin + c * self.rect.w, yorigin + l * self.rect.h)
        PhysicsObject.__init__(self)

    def update(self):
        pass

class Border(pygame.sprite.Sprite):

    def __init__(self, l, c):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('igloo.jpg')
        self.rect.move_ip(xorigin + c * self.rect.w, yorigin + l * self.rect.h)
    
    def update(self):
        pass

class Pingoo(pygame.sprite.Sprite, PhysicsObject):

    def __init__(self, l, c):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('tux.png', ALPHA)
        self.rect.move_ip(xorigin + c * self.rect.w, yorigin + l * self.rect.h)
        PhysicsObject.__init__(self, pixelsBySecondToSpeedUnit(100.0), 0.0)
        print self.vx
        self.key = 0

    def update(self):
        self.doPhysics()


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

#    if event.type == pygame.KEYUP:
#        undefine_move_if_equal(event.key)
#       return


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

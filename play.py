# This module defines the play state

import random
import pygame
from game import screen, load_image, xorigin, yorigin, ALPHA, COLORKEY_AUTO

nextT = 0
deltaT = 20

class PhysicsObject:

    def __init__(self):
        # position
        self.x = 0.0
        self.y = 0.0
        # speed in pixels/ms
        self.vx = 0.0
        self.vy = 0.0
        
    def doPhysics(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.left = self.x

class Block(pygame.sprite.Sprite, PhysicsObject):

    def __init__(self, l, c):
        pygame.sprite.Sprite.__init__(self)
        PhysicsObject.__init__(self)
        self.image, self.rect = load_image('glacon.png', COLORKEY_AUTO)
        self.rect.move_ip(xorigin + c * self.rect.w, yorigin + l * self.rect.h)

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
        PhysicsObject.__init__(self)
        self.vx = 2.5
        self.image, self.rect = load_image('tux.png', ALPHA)
        self.rect.move_ip(xorigin + c * self.rect.w, yorigin + l * self.rect.h)
        self.key = 0

    def update(self):
        self.doPhysics()


#font = pygame.font.Font(None, 50)

back = pygame.image.load("media/playbackground.png").convert()
#tux = pygame.image.load("media/tux.png").convert_alpha()

# Move should be computed on time (see clock) because tick is not stable
blocksize = 40
moveframes = 8
movesize = int(blocksize / moveframes)
motionticktime = int(100 / moveframes)
ticknumber = 0

lmax = 13
cmax = 19

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

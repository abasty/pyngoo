# This module defines the play state

import random
import pygame
from game import Object, MOTIONTICK, screen, load_image, xorigin, yorigin

class Block(pygame.sprite.Sprite):

    def __init__(self, l, c):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('glacon.png', -1)
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
#font = pygame.font.Font(None, 50)

back = pygame.image.load("media/playbackground.png").convert()
#glacon = pygame.image.load("media/glacon.png").convert()
#glacon.set_colorkey(glacon.get_at((0,0)), pygame.RLEACCEL)
#bord = pygame.image.load("media/igloo.jpg").convert()
#neige = pygame.image.load("media/neige.jpg").convert()
#tux = pygame.image.load("media/tux.png").convert_alpha()


# Move should be computed on time (see clock) because tick is not stable
blocksize = 40
moveframes = 8
movesize = int(blocksize / moveframes)
motionticktime = int(100 / moveframes)
ticknumber = 0

lmax = 13
cmax = 19

player = Object()

# Initialization
def init():
    pass

def enter():
    
    global labyrinth
    labyrinth = pygame.sprite.RenderPlain()

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

    for l in range(lmax):
        for c in range(cmax):
            p = tableau[l][c]
            if p is "b":
                labyrinth.add(Border(l, c))
            if p is "x":
                labyrinth.add(Block(l, c))
    
    pygame.time.set_timer(MOTIONTICK, motionticktime)

def leave():
    global labyrinth
    labyrinth.empty()
    pygame.time.set_timer(MOTIONTICK, 0)

def define_move(key):
    player.key = key

def undefine_move_if_equal(key):
    pass
#    if player.key == key:
#        player.key = -1

def begin_move():
    pass

def move():
    pass

def motiontick():
    global ticknumber
    if ticknumber == 0:
        begin_move()
    move()

    ticknumber = (ticknumber + 1) % moveframes

# Event callback
def event(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "Menu"
        elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            # try w/ sets (event.key in (...)
            define_move(event.key)
        return
    
#    if event.type == pygame.KEYUP:
#        undefine_move_if_equal(event.key)
#       return

    if event.type == MOTIONTICK:
        motiontick()

# Draw callback
def draw():
    screen.blit(back, [0, 0])

    # draw board
    labyrinth.draw(screen)
    # draw player
#    game.screen.blit(player.picture, [ player.x, player.y ])

init()

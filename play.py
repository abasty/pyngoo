# This module defines the play state

import random
import pygame
import math
from game import screen, load_image, xorigin, yorigin, ALPHA, COLORKEY_AUTO, inputMode, INPUT_KEYBOARD, INPUT_MOUSE

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

def pixelsPerSecondToSpeedUnit(pxBysec):
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
        self.velocityMax = pixelsPerSecondToSpeedUnit(velocityMaxInPixelsPerSeconds)
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

class Block(PhysicsSprite):
    """The class to represent a block"""

    STATE_JUST_PUSHED = 1
    STATE_PUSHED = 2
    STATE_DYING = 3

    def __init__(self, l, c):
        PhysicsSprite.__init__(self, l, c, 'glacon-animated.png', COLORKEY_AUTO, 8, 500.0)

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

    def update(self, t):
        if self.state == self.STATE_JUST_PUSHED:
            self.updatePhysics()
            hit = pygame.sprite.spritecollide(self, labyrinth, False)
            if len(hit) == 1:
                self.setState(self.STATE_PUSHED)
                return
            self.cancelPhysics()
            self.setState(self.STATE_DYING)
            self.startAnimation(t, range(1, 8), 25)
        elif self.state == self.STATE_PUSHED:
            self.updatePhysics()
            hit = pygame.sprite.spritecollide(self, labyrinth, False)
            if len(hit) == 1:
                return
            self.cancelPhysics()
            self.setState(self.STATE_NORMAL)
        elif self.state == self.STATE_DYING:
            self.updateAnimation(t)
            if self.currentIndex < 0:
                self.kill()

    def push(self, direction):
        if self.state == self.STATE_NORMAL:
            self.direction = direction
            self.setState(self.STATE_JUST_PUSHED)

class Border(PhysicsSprite):
    """The class to represent a border block"""
    def __init__(self, l, c):
        PhysicsSprite.__init__(self, l, c, 'igloo.jpg', None, 1, 1.0)

    def update(self, t):
        pass

class Diamond(PhysicsSprite):
    """The class to represent a diamond"""

    STATE_PUSHED = 2

    def __init__(self, l, c):
        PhysicsSprite.__init__(self, l, c, 'gift.png', ALPHA, 1, 500.0)

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

    def update(self, t):
        if self.state == self.STATE_PUSHED:
            self.updatePhysics()
            hit = pygame.sprite.spritecollide(self, labyrinth, False)
            if len(hit) == 1:
                return
            self.cancelPhysics()
            self.setState(self.STATE_NORMAL)

    def push(self, direction):
        if self.state == self.STATE_NORMAL:
            self.direction = direction
            self.setState(self.STATE_PUSHED)

class Pingoo(PhysicsSprite):
    """The pingoo/player class"""
    def __init__(self, l, c):
        PhysicsSprite.__init__(self, l, c, 'santa.png', ALPHA, 1, 250.0)
        self.pushing = False

    def updateTarget(self):
        # TODO: use something like int(self.target.y / self.rect.h + 1) * self.rect.h
        # TODO: a method like PhysicsSprite.setTargetFromPositionDirection()

        if inputMode == INPUT_KEYBOARD:
            keys = pygame.key.get_pressed()
            up = keys[pygame.K_UP]
            down = keys[pygame.K_DOWN]
            left = keys[pygame.K_LEFT]
            right = keys[pygame.K_RIGHT]
            self.pushing = keys[pygame.K_SPACE]
        elif inputMode == INPUT_MOUSE:
            mouseX, mouseY = pygame.mouse.get_pos()
            up = self.rect.centery - mouseY > self.rect.h / 1.5
            down = mouseY - self.rect.centery > self.rect.h / 1.5
            left = self.rect.centerx - mouseX > self.rect.w / 1.5
            right = mouseX - self.rect.centerx> self.rect.w / 1.5
            self.pushing = pygame.mouse.get_pressed()[0]
        
        if up:
            self.target.y -= self.rect.h
            self.direction = DIRECTION_UP
        elif down:
            self.target.y += self.rect.h
            self.direction = DIRECTION_DOWN
        elif left:
            self.target.x -= self.rect.w
            self.direction = DIRECTION_LEFT
        elif right:
            self.target.x += self.rect.w
            self.direction = DIRECTION_RIGHT
        else:
            self.target = Vector2d(self.position.x, self.position.y)
            self.direction = DIRECTION_NONE

    def update(self, t):
        self.updatePhysics()
        hit = pygame.sprite.spritecollide(self, labyrinth, False)
        if not hit:
            return
        if self.pushing:
            hit[0].push(self.direction)
        self.cancelPhysics()

# Initialization
def init():
    pass

def enter():
    global labyrinth, player, pingoo
    labyrinth = pygame.sprite.LayeredDirty()
    pingoo = Pingoo(lmax / 2, cmax / 2)
    player = pygame.sprite.LayeredDirty(pingoo)

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
    
    # room for the player
    tableau[lmax / 2][cmax / 2] = "."
    
    # create diamonds
    n = 0
    while n < 3:
        l = random.randrange(0, lmax / 2 - 1) * 2 + 2
        c = random.randrange(0, cmax / 2 - 1) * 2 + 2
        if tableau[l][c] == "X":
            continue
        tableau[l][c] = "X"
        n += 1

    #define sprites
    for l in range(lmax):
        for c in range(cmax):
            p = tableau[l][c]
            if p is "b":
                labyrinth.add(Border(l, c))
            if p is "x":
                labyrinth.add(Block(l, c))
            if p is "X":
                labyrinth.add(Diamond(l, c))

    global nextT, deltaT
    nextT = pygame.time.get_ticks() + deltaT
    
    if inputMode == INPUT_MOUSE:
        pygame.mouse.set_pos(pingoo.rect.centerx, pingoo.rect.centery)

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
    global nextT, deltaT, labyrinth, player
    t = pygame.time.get_ticks()
    labyrinth.clear(screen, back)
    player.clear(screen, back)
    while t >= nextT:
        player.update(t)
        labyrinth.update(t)
        nextT += deltaT
    labyrinth.draw(screen)
    player.draw(screen)

init()

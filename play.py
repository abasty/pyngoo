# This module defines the play state

import random
from pygame import Rect
from game import * #@UnusedWildImport
from physics import * #@UnusedWildImport

class PlayScreen:

    STATE_PLAYING = 0
    STATE_PAUSED = 1
    STATE_WON = 2

    level = 0
    score = 0

    back = pygame.image.load("media/background.png").convert()

    limits = Rect(xorigin, yorigin, cmax * 40, lmax * 40)
    gamezone = limits.inflate(-40 * 2, -40 * 2)

    def __init__(self):

        self.state = PlayScreen.STATE_PLAYING

        PlayScreen.level += 1
        random.seed(PlayScreen.level)

        self.all = pygame.sprite.LayeredDirty()
        self.labyrinth = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.diamonds = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()

        self.pingoo = Pingoo(lmax / 2, cmax / 2)
        self.pingoo.add(self.all, self.player)

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
                    Border(l, c).add(self.all, self.labyrinth, self.borders)
                if p is "x":
                    Block(l, c).add(self.all, self.labyrinth)
                if p is "X":
                    Diamond(l, c).add(self.all, self.labyrinth, self.diamonds)

        # counters
        self.scoreDisplay = CounterObject(352, 32, 6)
        self.scoreDisplay.value = PlayScreen.score
    
        Physics.t = pygame.time.get_ticks() + Physics.dt

        if inputMode == INPUT_MOUSE:
            pygame.mouse.set_pos(self.pingoo.rect.centerx, self.pingoo.rect.centery)

    def __del__(self):
        PlayScreen.score = self.scoreDisplay.value

    def endTest(self, a):
        global playscreen
        if a > 0:
            self.scoreDisplay.addValue(a * 5000, 25)
            pygame.mixer.music.load("media/jingle-bells.ogg")
            pygame.mixer.music.play(-1)
            self.state = PlayScreen.STATE_WON
            playscreen.window.show()
            playscreen.wonText.show()
            Border.setToBlinkBlink()

class Window(pygame.sprite.DirtySprite):

    def __init__(self, w, h, color=[0, 0, 0]):
        global playscreen
        self._layer = 99
        pygame.sprite.DirtySprite.__init__(self)
        self.visible = False
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.image.set_alpha(128)
        x, y = playscreen.gamezone.centerx - w / 2, playscreen.gamezone.centery - h / 2
        self.rect = Rect(x, y, w, h)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

class Text(pygame.sprite.DirtySprite):

    def __init__(self, message, color=white):
        self._layer = 100
        pygame.sprite.DirtySprite.__init__(self)
        self.visible = False
        self.setMessage(message, color)

    def _render(self):
        global playscreen
        font = pygame.font.Font(None, 100)
        self.image = font.render(self.message, True, self.color)
        w, h = self.image.get_size()
        x, y = playscreen.gamezone.centerx - w / 2, playscreen.gamezone.centery - h / 2
        self.rect = Rect(x, y, w, h)
        self.dirty = 1

    def setMessage(self, message="PLACE HOLDER", color=white):
        self.message = message
        self.color = color
        self._render()

    def setColor(self, color=white):
        self.color = color
        self._render()

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

class CounterObject:

    image = pygame.image.load("media/numbers.png").convert_alpha()
    fh = 26
    fw = 16
    # TODO: offset step for individual digit fs = 4

    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
        self.value = 0
        self.displayedValue = 0
        self.rect = Rect(self.x, self.y, self.fw * self.length, self.fh)
        self.step = 1000000

    def setValue(self, value, step = 10):
        self.value = value
        self.step = step

    def addValue(self, delta, step = 10):
        self.setValue(self.value + delta, step)

    def draw(self):
        delta = self.value - self.displayedValue
        if delta > 0:
            self.displayedValue += min(self.step, delta)
        elif delta < 0:
            self.displayedValue -= min(self.step, delta)
        n = self.displayedValue
        screen.blit(playscreen.back, self.rect, self.rect)
        for c in range(self.length - 1, -1, -1):
            d = n % 10
            screen.blit(self.image, [self.x + c * self.fw, self.y], Rect(0, d * self.fh, self.image.get_width(), self.fh))
            n = n // 10
        return [ self.rect ]

class Block(PhysicsSprite):
    """The class to represent a block"""

    STATE_JUST_PUSHED = 1
    STATE_PUSHED = 2
    STATE_DYING = 3

    sound = pygame.mixer.Sound("media/ice.ogg")
    soundbreak = pygame.mixer.Sound("media/glassbroken.wav")

    def __init__(self, l, c):
#        PhysicsSprite.__init__(self, l, c, 'glacon-animated.png', TRANSPARENCY_COLORKEY_AUTO, 8, 500.0)
        PhysicsSprite.__init__(self, l, c, 'ball.png', TRANSPARENCY_ALPHA, 40, 40, 500.0)

    def updateTarget(self, t):
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

    def updateFrame(self):
        X = self.position.x - playscreen.gamezone.left
        S = int((X % 40) / 5)
        self.setFrame(S + 0)

    def update(self, t):
        if self.state == self.STATE_NORMAL:
            self.updateFrame()
        elif self.state == self.STATE_JUST_PUSHED:
            self.updatePhysics(t)
            hit = pygame.sprite.spritecollide(self, playscreen.labyrinth, False)
            if len(hit) == 1:
                self.setState(self.STATE_PUSHED)
                self.updateFrame()
                self.sound.play(-1)
                return
            self.cancelPhysics()
            self.updateFrame()
            self.setState(self.STATE_DYING)
            self.soundbreak.play()
            self.startAnimation(t, range(8, 12), 15)
        elif self.state == self.STATE_PUSHED:
            self.updatePhysics(t)
            self.updateFrame()
            hit = pygame.sprite.spritecollide(self, playscreen.labyrinth, False)
            if len(hit) == 1:
                return
            self.cancelPhysics()
            self.updateFrame()
            self.setState(self.STATE_NORMAL)
            self.sound.stop()
        elif self.state == self.STATE_DYING:
            self.updateAnimation(t)
            if self.animationStopped():
                self.kill()
                playscreen.scoreDisplay.addValue(10, 1)

    def push(self, direction):
        if self.state == self.STATE_NORMAL:
            self.direction = direction
            self.setState(self.STATE_JUST_PUSHED)

class Border(PhysicsSprite):

    STATE_BLINKBLINK = 1

    """The class to represent a border block"""
    def __init__(self, l, c):
        PhysicsSprite.__init__(self, l, c, 'trees.png', TRANSPARENCY_COLORKEY_AUTO, 40, 40, 400.0)
#        self.setFrame(random.randrange(16))
        self.setFrame(random.choice([0, 1, 2, 3, 7, 8, 9, 10, 12]))

    @classmethod
    def setToBlinkBlink(cls):
        for b in playscreen.borders:
            b.setState(Border.STATE_BLINKBLINK)

    def updateTarget(self, t):
        if self.state == self.STATE_NORMAL:
            return

        l, c = self.getLC()
        if c == 0 and l != 0:
            self.target.y = self.position.y - self.rect.h
        if l == 0 and c != cmax - 1:
            self.target.x = self.position.x + self.rect.w
        if c == cmax - 1 and l != lmax -1:
            self.target.y = self.position.y + self.rect.h
        if l == lmax - 1 and c != 0:
            self.target.x = self.position.x - self.rect.w

    def update(self, t):
        self.updatePhysics(t)

class Diamond(PhysicsSprite):
    """The class to represent a diamond"""

    STATE_PUSHED = 2

    def __init__(self, l, c):
        PhysicsSprite.__init__(self, l, c, 'gift.png', TRANSPARENCY_ALPHA, 40, 40, 500.0)

    @classmethod
    def aligned(cls):
        global diamonds
        d = playscreen.diamonds.sprites()
        r0 = pygame.Rect(d[0].rect)
        u = r0.unionall((d[1].rect, d[2].rect))
        if (u.w != r0.w or u.h != r0.h * 3) and (u.h != r0.h or u.w != 3 * r0.w):
            return 0, u
        if u.top == playscreen.gamezone.top or u.bottom == playscreen.gamezone.bottom or u.left == playscreen.gamezone.left or u.right == playscreen.gamezone.right:
            return 1, u
        return 2, u

    def updateTarget(self, t):
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
            self.updatePhysics(t)
            hit = pygame.sprite.spritecollide(self, playscreen.labyrinth, False)
            if len(hit) == 1:
                return
            self.cancelPhysics()
            self.setState(self.STATE_NORMAL)
            a, _u = self.aligned()
            playscreen.endTest(a)
                
    def push(self, direction):
        if self.state == self.STATE_NORMAL:
            self.direction = direction
            self.setState(self.STATE_PUSHED)

class Monster(PhysicsSprite):
    """The class to represent a diamond"""

    STATE_PUSHED = 2

    def __init__(self, l, c):
        PhysicsSprite.__init__(self, l, c, 'gift.png', TRANSPARENCY_ALPHA, 40, 40, 500.0)

    def updateTarget(self, t):
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
            self.updatePhysics(t)
            hit = pygame.sprite.spritecollide(self, playscreen.labyrinth, False)
            if len(hit) == 1:
                return
            self.cancelPhysics()
            self.setState(self.STATE_NORMAL)

class Pingoo(PhysicsSprite):
    """The pingoo/player class"""
    def __init__(self, l, c):
        PhysicsSprite.__init__(self, l, c, 'santa2.png', TRANSPARENCY_COLORKEY_AUTO, 40, 40, 250.0)
        self.pushing = False

    def updateTarget(self, t):
        if playscreen.state != PlayScreen.STATE_PLAYING:
            up = False
            down = False
            left = False
            right = False
            self.pushing = False
        elif inputMode == INPUT_KEYBOARD:
            keys = pygame.key.get_pressed()
            up = keys[pygame.K_UP]
            down = keys[pygame.K_DOWN]
            left = keys[pygame.K_LEFT]
            right = keys[pygame.K_RIGHT]
            self.pushing = keys[pygame.K_SPACE]
        elif inputMode == INPUT_MOUSE:
            mouseX, mouseY = pygame.mouse.get_pos()
            lmax = 15
            up = pygame.Rect(self.rect.left, self.rect.top - lmax * self.rect.h, self.rect.w, lmax * self.rect.h).collidepoint(mouseX, mouseY)
            down = pygame.Rect(self.rect.left, self.rect.top + self.rect.h, self.rect.w, lmax * self.rect.h).collidepoint(mouseX, mouseY)
            left = pygame.Rect(self.rect.left - lmax * self.rect.w, self.rect.top, lmax * self.rect.w, self.rect.h).collidepoint(mouseX, mouseY)
            right = pygame.Rect(self.rect.left + self.rect.w, self.rect.top, lmax * self.rect.w, self.rect.h).collidepoint(mouseX, mouseY)
            self.pushing = pygame.mouse.get_pressed()[0]

        # TODO: use something like int(self.target.y / self.rect.h + 1) * self.rect.h
        # TODO: a method like PhysicsSprite.setTargetFromPositionDirection()
        _old = self.direction
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

        if _old != self.direction:
            if self.direction == DIRECTION_UP:
                _frame = 0
            elif self.direction == DIRECTION_DOWN:
                _frame = 6
            elif self.direction == DIRECTION_LEFT:
                _frame = 9
            elif self.direction == DIRECTION_RIGHT:
                _frame = 3
            else:
                _frame = -1
            if _frame >= 0:
                self.startAnimation(t, range(_frame, _frame + 3), 14, True)
            else:
                self.endAnimation()

    def update(self, t):
        global playscreen
        self.updatePhysics(t)
        self.updateAnimation(t)
        hit = pygame.sprite.spritecollide(self, playscreen.labyrinth, False)
        if not hit:
            return
        if self.pushing:
            hit[0].push(self.direction)
        self.cancelPhysics()
        self.updateAnimation(t)

def enter():
    global playscreen
    playscreen = PlayScreen()
    # Messages
    playscreen.window = Window(600, 400)
    playscreen.window.add(playscreen.all)
    playscreen.pauseText = Text("Game is paused")
    playscreen.pauseText.add(playscreen.all)
    playscreen.wonText = Text("Well Done !") 
    playscreen.wonText.add(playscreen.all)

def leave():
    global playscreen
    del playscreen
    pygame.mixer.music.stop()

# Event callback
def event(event):
    global playscreen
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return "Menu"
        elif event.key == pygame.K_n:
            return "Next"
        elif event.key == pygame.K_b:
            if playscreen.state == PlayScreen.STATE_PLAYING:
                playscreen.state = PlayScreen.STATE_PAUSED
                playscreen.window.show()
                playscreen.pauseText.show()
            elif playscreen.state == PlayScreen.STATE_PAUSED:
                playscreen.state = PlayScreen.STATE_PLAYING
                playscreen.window.hide()
                playscreen.pauseText.hide()
        elif event.key == pygame.K_p:
            pygame.image.save(screen, "pyngoo.png")
        return

# Draw callback
def draw():
    global playscreen

    # Clear stuff
    playscreen.all.clear(screen, playscreen.back)

    # Run physics
    t = pygame.time.get_ticks()
    while t >= Physics.t:
        playscreen.player.update(t)
        playscreen.labyrinth.update(t)
        Physics.t += Physics.dt

    # Manage won state message color
    if playscreen.state == PlayScreen.STATE_WON:
        playscreen.wonText.setColor([random.randrange(256), random.randrange(256), random.randrange(256)])

    # Draw stuff
    _res = playscreen.all.draw(screen)
    # Draw score
    _res += playscreen.scoreDisplay.draw()

    return _res

import pygame
from game import load_image, xorigin, yorigin

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
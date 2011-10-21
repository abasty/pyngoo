#!/usr/bin/python

import pygame
pygame.init()

import game
import mainmenu
 
done = False
clock = pygame.time.Clock()
screen = mainmenu
 
while not done:

    # Dispatch event to current screen and handle QUIT event
    for event in pygame.event.get():
        if screen.event(event) == "Quit":
            done = True;
        if event.type == pygame.QUIT:
            done = True 

    # Draw current screen	
    screen.draw()
    
    # Manage frame and frame rate
    pygame.display.flip()
    clock.tick(10)
 
# Be IDLE friendly
print "Ending game..."
pygame.quit ()
print "The End."


#!/usr/bin/python

import pygame
pygame.init()

#import game
import mainmenu
import play
import setup
import about

done = False
clock = pygame.time.Clock()
screen = mainmenu

while not done:

    # Dispatch event to current screen and handle QUIT event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True 
        else:
            trans = screen.event(event)
            if trans == "Quit":
                done = True;
            elif trans == "Play":
                screen = play
            elif trans == "Menu":
                screen = mainmenu
            elif trans == "Setup":
                screen = setup
            elif trans == "About":
                screen = about

    # Draw current screen	
    screen.draw()

    # Manage frame and frame rate
    pygame.display.flip()
    clock.tick(10)
 
# Be IDLE friendly
print "Ending game..."
pygame.quit ()
print "The End."


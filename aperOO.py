#!/usr/bin/python

import pygame
pygame.init()

import game
import mainmenu
import play
import setup
import about

done = False
clock = pygame.time.Clock()
screen = 0

def enterScreen(s):
    global screen
    if screen != 0:
        screen.leave()
    screen = s
    screen.enter()

def handleScreenEvent(event):
    global screen
    return screen.event(event)

def drawScreen():
    global screen
    screen.draw()

enterScreen(play)

while not done:
    # Dispatch event to current screen and handle QUIT event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True 
        else:
            trans = handleScreenEvent(event)
            if trans == "Quit":
                done = True;
            elif trans == "Play":
                enterScreen(play)
            elif trans == "Menu":
                enterScreen(mainmenu)
            elif trans == "Setup":
                enterScreen(setup)
            elif trans == "About":
                enterScreen(about)
                
    if done:
        break

    # Draw current screen    
    drawScreen()

    # Manage frame and frame rate
    pygame.display.flip()
    clock.tick(20)

# Be IDLE friendly
print "Ending game..."
pygame.quit()
print "The End."


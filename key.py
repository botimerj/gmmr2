# import the pygame module, so you can use it
import pygame
import numpy as np
from enum import IntEnum


SCREEN_SIZE = (960,540)
            
def draw_logo(): 
    logo = pygame.Surface((32,32)) 
    pxarr = pygame.PixelArray(logo)
    for y in range(32) : 
        for x in range(32) : 
            #pxarr[x,y] = (255,255-8*x,255-8*y)
            pxarr[x,y] = (255,(x+y)*4,255-(x+4)*4)
    pxarr.close()
    return logo

# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = draw_logo()
    #logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Key press")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.KEYDOWN: 
                print(event.key)
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

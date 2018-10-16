import pygame

def draw_logo(): 
    logo = pygame.Surface((32,32)) 
    pxarr = pygame.PixelArray(logo)
    for y in range(32) : 
        for x in range(32) : 
            #pxarr[x,y] = (255,255-8*x,255-8*y)
            pxarr[x,y] = (255,(x+y)*4,255-(x+4)*4)
    pxarr.close()
    return logo

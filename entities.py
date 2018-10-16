import numpy as np
import pygame
import random as rand


class Player():
    def __init__(self):
        self.type   = 'player'
        self.radius = 10 
        self.color  = (132,40,230) 
        self.image  = circle(self.radius,self.color)
        self.coor   = (250,0)
        self.rect   = ((self.coor[0]-self.radius,self.coor[1]-self.radius),\
                       (self.coor[0]+self.radius,self.coor[1]+self.radius))
        self.velocity = (1,1) 
 
class Planet():
    def __init__(self, radius = None, color = None, coor = None) :
        self.type   = 'planet'
        if radius is None:
            self.radius = rand.randint(250,750)
        else : 
            self.radius = radius 
        if color is None:
            self.color  = (rand.randint(0,255),rand.randint(0,255),rand.randint(0,255))
        else : 
            self.color  = color
        if coor is None:
            self.coor   = (rand.randint(-SCREEN_SIZE[0]/2,SCREEN_SIZE[0]/2),\
                           rand.randint(-SCREEN_SIZE[1]/2,SCREEN_SIZE[1]/2))
        else : 
            self.coor   = coor 

        self.rect   = ((self.coor[0]-self.radius,self.coor[1]-self.radius),\
                       (self.coor[0]+self.radius,self.coor[1]+self.radius))

        self.px_radius = int(self.radius/10)
        self.px_loc    = (int(self.coor[0]/10)+CENTER[0]-self.px_radius,\
                          int(self.coor[1]/10)+CENTER[1]-self.px_radius)
        self.visible   = on_screen(self.px_loc) 
        self.image = pygame.Surface((self.px_radius*2-1,self.px_radius*2-1))
        self.image.set_colorkey((255,255,255))
        self.image.fill((255,255,255))
        pygame.draw.circle(self.image,self.color,(self.px_radius,self.px_radius),self.px_radius)
   

    def zoom(self, zoom, focus) :
        self.px_radius = int(self.radius/zoom)
        self.image = pygame.Surface((self.px_radius*2-1,self.px_radius*2-1))
        self.image.set_colorkey((255,255,255))
        self.image.fill((255,255,255))
        pygame.draw.circle(self.image,self.color,(self.px_radius,self.px_radius),self.px_radius)
        self.move(zoom,focus)

    def move(self, zoom, focus) : 
        self.px_loc    = (int(self.coor[0]/zoom - focus[0])+CENTER[0]-self.px_radius,\
                          int(self.coor[1]/zoom - focus[1])+CENTER[1]-self.px_radius)
        self.visible   = on_screen(self.px_loc) 

   

def distance(a,b):
    return np.sqrt((a[1]-b[1])**2+(a[0]-b[0])**2)

def circle(radius, color):
    square_dim = radius*2-1
    center = (radius-1,radius-1)
    new_surface = pygame.Surface((square_dim,square_dim))
    new_surface.set_colorkey((255,255,255))
    pxarr = pygame.PixelArray(new_surface)
    for y in range(square_dim) : 
        for x in range(square_dim) : 
            if distance(center, (x,y)) <= radius-1 : 
                pxarr[y,x] = color 
            else :
                pxarr[y,x] = (255,255,255) 
    pxarr.close()
    new_surface.convert()
    return new_surface 
 

def main() : 
    print("Entities")

if __name__=="__main__" : 
    # Do Nothing
    main()



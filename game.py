# import the pygame module, so you can use it
import pygame
import numpy as np
import random as rand

#SCREEN_SIZE = (960,540)
SCREEN_SIZE = (1440,810)
#SCREEN_SIZE = (1920,1080)


def draw_logo(): 
    logo = pygame.Surface((32,32)) 
    pxarr = pygame.PixelArray(logo)
    for y in range(32) : 
        for x in range(32) : 
            #pxarr[x,y] = (255,255-8*x,255-8*y)
            pxarr[x,y] = (255,(x+y)*4,255-(x+4)*4)
    pxarr.close()
    return logo

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
            self.radius = rand.randint(25,75)
        else : 
            self.radius = radius 
        if color is None:
            self.color  = (rand.randint(0,255),rand.randint(0,255),rand.randint(0,255))
        else : 
            self.color  = color
        if coor is None:
            self.coor   = (rand.randint(-SCREEN_SIZE[0]/2,SCREEN_SIZE[0]/20),\
                           rand.randint(-SCREEN_SIZE[1]/2,SCREEN_SIZE[1]/20))
        else : 
            self.coor   = coor 

        self.image  = circle(int(self.radius/10),self.color)
        self.rect   = ((self.coor[0]-int(self.radius/10),self.coor[1]-int(self.radius/10)),\
                       (self.coor[0]+int(self.radius/10),self.coor[1]+int(self.radius/10)))
                       
    def update_img(self, zoom) : 
        self.image  = circle(int(self.radius/zoom),self.color)
        self.rect   = ((self.coor[0]-int(self.radius/10),self.coor[1]-int(self.radius/10)),\
                       (self.coor[0]+int(self.radius/10),self.coor[1]+int(self.radius/10)))
   
class Image(): 
    def __init__(self) : 
        self.focus = (0,0)
        self.zoom  = 10  # Meters/Pixel 
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.background = pygame.transform.scale(pygame.image.load("stars.png"),SCREEN_SIZE)
        self.background.convert()
    
    def init_screen(self, entities) : 
        self.screen.blit(self.background,(0,0))
        for entity in entities :
            self.screen.blit(entity.image,self.px_coor(self.focus,entity.rect[0]))
        pygame.display.flip() 

    def px_coor(self, focus, entity_coor) : 
        # 1:1 px to coor DOES NOT WORRY ABOUT FOCUS ATM
        return (SCREEN_SIZE[0]/2+entity_coor[0],SCREEN_SIZE[1]/2+entity_coor[1]) 
    
    def update_zoom(self, entities, direction) :
        if self.zoom > 1 : 
            if direction : # Zoom out
                self.zoom += 1
                for entity in entities : 
                    entity.update_img(self.zoom) 
            else : 
                self.zoom -= 1
                for entity in entities : 
                    entity.update_img(self.zoom) 

            self.init_screen(entities) # Update screen
            
   
class GameState():
    def __init__(self):
        self.image = Image() 
        self.entities = self.init_entities()
        self.image.init_screen(self.entities) 
        
   
    def init_entities(self) : 
        ent_arr = []
        ent_arr.append(Planet(radius=2000,coor=(0,0)))
        ent_arr.append(Planet(radius=200,coor=(500,0)))
        return ent_arr
        
    def scroll(self, direction) : 
        image.update_zoom(entities, direction) 
        


# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = draw_logo()
    #logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")
     
    # create a surface on screen that has the size of 240 x 180
    gamestate = GameState()
     
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
            elif event.type == pygame.MOUSEBUTTONDOWN : 
                print(event.button)
                if event.button == 4 : gamestate.scroll(0) # Zoom in
                if event.button == 5 : gamestate.scroll(1) # Zoom out
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

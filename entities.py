# import the pygame module, so you can use it
import pygame
import numpy as np
import random as rand

SCREEN_SIZE = (1440,810)
CENTER = (int(SCREEN_SIZE[0]/2),int(SCREEN_SIZE[1]/2))
WHITE = 0xFFFFFF 
BLACK = 0x000000

class Body():
    def __init__(self, body_type = 'Body',\
                       color     = None,\
                       coor      = None,\
                       radius    = None,\
                       density   = None,\
                       velocity  = None):
        self.type   = body_type
        self.id     = rand.randint(0,2**32)
        if color is None : self.color  = (rand.randint(50,255),rand.randint(50,255),rand.randint(50,255))
        else             : self.color  = color
        if coor is None : self.coor = [rand.randint(-16000,16000),\
                                       rand.randint(-16000,16000)]
        else            : self.coor = coor 

        if radius is None : self.radius = rand.randint(50,2000)
        else              : self.radius = radius 
        if velocity is None : self.velocity = (0,0)
        else                : self.velocity = velocity
        if density is None : self.density = 1 
        else               : self.density = density

        self.mass     = self.radius*self.density 
        self.forces   = np.empty([1,2])
        self.accel    = np.empty(2)
   
        # Image information
        self.visible   = False
        self.px_radius = None # Radius in pixels
        self.px_ul     = None # upper left location
        self.image     = None

        # Stats
        self.collisions = 0

    def draw(self, zoom, focus) :
        self.px_radius = int(self.radius/zoom)
        self.move(zoom,focus)       # Update upper left location
        
        if self.visible : 
            if self.px_radius != 0 : 
                self.image = pygame.Surface((self.px_radius*2-1,self.px_radius*2-1))
            else : 
                self.image = pygame.Surface((1,1))
            self.image.set_colorkey((255,255,255))
            self.image.fill((255,255,255))
            pygame.draw.circle(self.image,self.color,(self.px_radius,self.px_radius),self.px_radius)

    def move(self, zoom, focus) : 
        self.px_ul     = [CENTER[0]+int(self.coor[0]/zoom - focus[0]/zoom)-self.px_radius,\
                          CENTER[1]-int(self.coor[1]/zoom - focus[1]/zoom)-self.px_radius]
        px_dim = self.px_radius*2-1 # Dimensions of surface
        top_left = self.px_ul
        bottom_right = [top_left[0]+px_dim,top_left[1]+px_dim]
        self.visible = on_screen([top_left,bottom_right])
    
    def physics(self,dt,zoom,focus) : 
        self.accel = np.sum(self.forces,axis=0)/self.mass
        self.velocity = (self.velocity[0]+self.accel[0]*dt, self.velocity[1]+self.accel[1]*dt)
        self.coor = [self.coor[0]+self.velocity[0]*dt, self.coor[1]+self.velocity[1]*dt]
        self.move(zoom, focus)
   

    
def on_screen(rect) : 
    if rect[0][0] < SCREEN_SIZE[0] and rect[0][1] < SCREEN_SIZE[1] :
        if rect[1][0] > 0 and rect[1][1] > 0 :
            return True
    return False
    
  
class Grid() :  
    def __init__(self,zoom,focus) :
        self.grid_space = 10000 #1000 meters
        self.grid_enable = True
        self.y_grid_loc = []
        self.x_grid_loc = []
        self.update(zoom,focus)

    def update(self,zoom,focus) : 
        #zoom_level = np.floor(zoom/20) + 1 
        #self.grid_space = 1000*(zoom_level)
        pixel_step = int(self.grid_space/zoom)

        offset_x = CENTER[0]-int(focus[0]/zoom)%pixel_step   
        offset_y = CENTER[1]+int(focus[1]/zoom)%pixel_step   
        self.y_grid_loc = list(range(offset_y,SCREEN_SIZE[1]-1,pixel_step))+\
                          list(range(offset_y-pixel_step,0,-pixel_step))
        self.x_grid_loc = list(range(offset_x,SCREEN_SIZE[0]-1,pixel_step))+\
                          list(range(offset_x-pixel_step,0,-pixel_step))
        #print('zoom = ', zoom, '  focus = ', focus)

    def draw(self) : 
        grid  = pygame.Surface(SCREEN_SIZE) 
        grid.fill((20,20,20))
        pxarr = pygame.PixelArray(grid)
        for i in range(len(self.y_grid_loc)) : 
            if self.y_grid_loc[i] < SCREEN_SIZE[1]-1 and self.y_grid_loc[i] >= 0 :
                pxarr[:,self.y_grid_loc[i]] = WHITE 
        for i in range(len(self.x_grid_loc)) : 
            if self.x_grid_loc[i] < SCREEN_SIZE[0]-1 and self.x_grid_loc[i] >= 0 :
                pxarr[self.x_grid_loc[i],:] = WHITE 
        pxarr.close()
        return grid  

# define a main function
def main():
    print('Entities') 
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

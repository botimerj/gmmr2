# import the pygame module, so you can use it
import pygame
import numpy as np
import random as rand
import config 

#config.CENTER = (int(config.SCREEN_SIZE[0]/2),int(config.SCREEN_SIZE[1]/2))

#class Player() : 


class Cluster():
    def __init__(self,ent_list) :
        self.ent_list = ent_list
        self.coor = self.center_calc()
        self.velocity = self.velocity_calc()
    
    def center_calc(self):
        for i in range(len(self.ent_list)):
            center += self.ent_list[i].coor

    def velocity_calc(self):
        for i in range(len(self.ent_list)):
            velocity += self.ent_list[i].velocity

    def remove(self, ent):
        if ent in self.ent_list:
            self.ent_list.remove(ent)
            ent.in_cluster = False 
        self.center_calc()
        self.velocity_calc()

    def add(self, ent):
        if ent not in self.ent_list:
            if ent.in_cluster : 
                self.ent_list.append(ent)
                ent.in_cluster = True
        self.center_calc()
        self.velocity_calc()
    

class Body():
    def __init__(self, name = 'Body',\
                       color     = None,\
                       coor      = None,\
                       radius    = None,\
                       density   = None,\
                       velocity  = None):
        
        # Identifiers
        self.name   = name 
        self.id     = rand.randint(1,2**32)
        if color is None : self.color  = (rand.randint(50,255),\
                                          rand.randint(50,255),\
                                          rand.randint(50,255))
        else             : self.color  = color

        # Physics
        if coor is None : self.coor = [0,0]
        else            : self.coor = coor 
        if radius is None : self.radius = rand.randint(10,200)
        else              : self.radius = radius 
        if velocity is None : self.velocity = [0,0]
        else                : self.velocity = velocity
        if density is None : self.density = 1 
        else               : self.density = density
        self.mass     = self.radius*self.density 
        self.forces   = np.zeros([1,2])
        self.accel    = np.zeros(2)
        
        # Approx physics
        self.influences = [] 

        # Collision
        self.touching = []
        self.in_cluster = False
    
        # Image information
        self.visible   = True 
        self.px_radius = None # Radius in pixels
        self.px_ul     = None # upper left location
        self.image     = pygame.Surface((1,1)) 

        # Stats
        self.collisions = 0

    def draw(self, zoom, focus) :
        self.px_radius = int(self.radius/zoom)
        
        image_dim = self.px_radius*2-1
        small_img =  image_dim < config.SCREEN_SIZE[0] and image_dim < config.SCREEN_SIZE[1] 
        c_px = None
        c_rel = None
        
        if self.visible : 
            if self.px_radius != 0 : 
                if small_img :  
                    self.image = pygame.Surface((image_dim,image_dim))
                else : # If planet is bigger than the screen
                    self.image = pygame.Surface(config.SCREEN_SIZE)
            else : # Always render body as at least 1 pixel 
                image_dim = 1 
                self.image = pygame.Surface((1,1))

            # Initialize image 
            self.image.set_colorkey((255,255,255))
            self.image.fill((255,255,255))

            # Draw circle
            if small_img :  
                pygame.draw.circle(self.image,self.color,(self.px_radius,self.px_radius),self.px_radius)
            else : # If planet is bigger than the screen
                c_rel = [focus[0] - self.coor[0], focus[1] - self.coor[1]]
                c_px  = [-int(c_rel[0]/zoom)+config.CENTER[0], int(c_rel[1]/zoom)+config.CENTER[1]]
                #print('c_rel = ', c_rel, 'c_px = ', c_px, 'px_radius = ', self.px_radius)
                pygame.draw.circle(self.image,self.color,c_px,self.px_radius)

        # Print stats
        #print('---Draw Stats---')
        #print('visible             = ', self.visible)
        #print('smaller than screen = ', small_img)
        #print('c_px                = ', c_px)
        #print('px_radius           = ', self.px_radius)

    def move(self, zoom, focus) : 
        image_dim = self.px_radius*2-1
        if image_dim < config.SCREEN_SIZE[0] and image_dim < config.SCREEN_SIZE[1] :  
            self.px_ul     = [config.CENTER[0]+int(self.coor[0]/zoom - focus[0]/zoom)-self.px_radius,\
                              config.CENTER[1]-int(self.coor[1]/zoom - focus[1]/zoom)-self.px_radius]
            px_dim = self.px_radius*2-1 # Dimensions of surface
            top_left = self.px_ul
            bottom_right = [top_left[0]+px_dim,top_left[1]+px_dim]
            self.visible = on_screen([top_left,bottom_right])
        else : # Image bigger than screen
            self.px_ul = (0,0)

            # Enclose focus in a circle and check if body px radius intersects with it
            focus_radius = config.SCREEN_SIZE[0]*zoom
            if distance(focus, self.coor) > (self.radius+focus_radius) : 
                self.visible = False 
            else : 
                self.visible = True
                self.image.fill((255,255,255))
                c_rel = [focus[0] - self.coor[0], focus[1] - self.coor[1]]
                c_px  = [-int(c_rel[0]/zoom)+config.CENTER[0], int(c_rel[1]/zoom)+config.CENTER[1]]
                pygame.draw.circle(self.image,self.color,c_px,self.px_radius)
                #self.draw(zoom, focus)
    
    def physics(self,dt,zoom,focus) : 
        self.accel = np.sum(self.forces,axis=0)/self.mass
        self.velocity = [self.velocity[0]+self.accel[0]*dt, self.velocity[1]+self.accel[1]*dt]
        self.coor = [self.coor[0]+self.velocity[0]*dt, self.coor[1]+self.velocity[1]*dt]
        #self.coor = [self.coor[0]+self.velocity[0]*dt+1/2*self.accel[0]*dt**2,\
        #             self.coor[1]+self.velocity[1]*dt+1/2*self.accel[1]*dt**2]
        self.move(zoom, focus)
    
    def print_stat(self) : 
        print('Name : ', self.type)
        print('accel: ', self.accel)
        print('vel  : ', self.velocity)
        print('------')
   
   

    
def on_screen(rect) : 
    if rect[0][0] < config.SCREEN_SIZE[0] and rect[0][1] < config.SCREEN_SIZE[1] :
        if rect[1][0] > 0 and rect[1][1] > 0 :
            return True
    return False
    
  
class Grid() :  
    def __init__(self,zoom,focus) :
        self.grid_space = 1e20  #1000 meters meters
        self.grid_enable = True
        self.y_grid_loc = []
        self.x_grid_loc = []
        self.update(zoom,focus)

    def update(self,zoom,focus) : 
        pixel_step = int(self.grid_space/zoom)
        if(pixel_step < 10):
            self.grid_space *= 10
        elif(pixel_step > 1000):
            self.grid_space /= 10
        pixel_step = int(self.grid_space/zoom)

        offset_x = config.CENTER[0]-int(focus[0]/zoom)%pixel_step   
        offset_y = config.CENTER[1]+int(focus[1]/zoom)%pixel_step   
        self.y_grid_loc = list(range(offset_y,config.SCREEN_SIZE[1]-1,pixel_step))+\
                          list(range(offset_y-pixel_step,0,-pixel_step))
        self.x_grid_loc = list(range(offset_x,config.SCREEN_SIZE[0]-1,pixel_step))+\
                          list(range(offset_x-pixel_step,0,-pixel_step))
        #print('zoom = ', zoom, '  focus = ', focus)

    def draw(self) : 
        grid  = pygame.Surface(config.SCREEN_SIZE) 
        grid.fill((20,20,20))
        pxarr = pygame.PixelArray(grid)
        for i in range(len(self.y_grid_loc)) : 
            if self.y_grid_loc[i] < config.SCREEN_SIZE[1]-1 and self.y_grid_loc[i] >= 0 :
                pxarr[:,self.y_grid_loc[i]] = config.WHITE 
        for i in range(len(self.x_grid_loc)) : 
            if self.x_grid_loc[i] < config.SCREEN_SIZE[0]-1 and self.x_grid_loc[i] >= 0 :
                pxarr[self.x_grid_loc[i],:] = config.WHITE 
        pxarr.close()
        return grid  

def distance(a,b):
    return np.sqrt((a[1]-b[1])**2+(a[0]-b[0])**2)

# define a main function
def main():
    print('Entities') 
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

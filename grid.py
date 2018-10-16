# import the pygame module, so you can use it
import pygame
import numpy as np
import random as rand
from logo import draw_logo

#SCREEN_SIZE = (960,540)
SCREEN_SIZE = (1440,810)
#SCREEN_SIZE = (1920,1080)
CENTER = (int(SCREEN_SIZE[0]/2),int(SCREEN_SIZE[1]/2))
WHITE = 0xFFFFFF 
BLACK = 0x000000
G = 1

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
    def __init__(self, radius = None, color = None,\
                 coor = None, velocity = None, density = None) :
        self.type   = 'planet'
        if radius is None : self.radius = rand.randint(100,500)
        else              : self.radius = radius 

        if color is None : self.color  = (rand.randint(50,255),rand.randint(50,255),rand.randint(50,255))
        else             : self.color  = color

        if coor is None : self.coor = [rand.randint(-16000,16000),\
                                       rand.randint(-16000,16000)]
                                    #(rand.randint(-SCREEN_SIZE[0]/2,SCREEN_SIZE[0]/2),\
                                    # rand.randint(-SCREEN_SIZE[1]/2,SCREEN_SIZE[1]/2))
        else            : self.coor = coor 

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

        #(0.100,0) #meters/milliseconds
        if velocity is None : 
            self.velocity = [rand.random()*np.sign(-self.coor[1])*5,rand.random()*np.sign(self.coor[0])*5]
        else                : self.velocity = velocity
        
        if density is None : self.density = 10
        else               : self.density = density

        self.mass     = self.radius*self.density # 100kg
        self.forces   = np.zeros([1,2])
        self.accel    = np.zeros(2)
   

    def zoom(self, zoom, focus) :
        self.px_radius = int(self.radius/zoom)
        if self.px_radius != 0 : 
            self.image = pygame.Surface((self.px_radius*2-1,self.px_radius*2-1))
        else : 
            self.image = pygame.Surface((1,1))
            
        self.image.set_colorkey((255,255,255))
        self.image.fill((255,255,255))
        pygame.draw.circle(self.image,self.color,(self.px_radius,self.px_radius),self.px_radius)
        self.move(zoom,focus)

    def move(self, zoom, focus) : 
        self.px_loc    = (CENTER[0]+int(self.coor[0]/zoom - focus[0]/zoom)-self.px_radius,\
                          CENTER[1]-int(self.coor[1]/zoom - focus[1]/zoom)-self.px_radius)
    
    def physics(self,dt,zoom,focus) : 
        self.accel = np.sum(self.forces,axis=0)/self.mass
        self.velocity = (self.velocity[0]+self.accel[0]*dt, self.velocity[1]+self.accel[1]*dt)
        self.coor = [self.coor[0]+self.velocity[0]*dt, self.coor[1]+self.velocity[1]*dt]
        self.move(zoom, focus)
   

    
def on_screen(loc) : 
    if (loc[0] > 0 or loc[0] < SCREEN_SIZE[0]) and\
       (loc[1] > 0 or loc[1] < SCREEN_SIZE[1]) : 
        return True
    return False
    
  
class Grid() :  
    def __init__(self,zoom,focus) :
        self.grid_space = 10000 #1000 meters
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
            pxarr[:,self.y_grid_loc[i]] = WHITE 
        for i in range(len(self.x_grid_loc)) : 
            pxarr[self.x_grid_loc[i],:] = WHITE 
        pxarr.close()
        return grid  

class Image(): 
    def __init__(self) : 
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
    
    def init(self,grid,entities) : 
        self.screen.fill((0,0,0))
        self.screen.blit(grid.draw(),(0,0))
        for entity in entities : 
            self.screen.blit(entity.image,entity.px_loc)
        pygame.display.flip() 

    def update(self,grid,entities,focus) : 
        self.screen.fill((0,0,0))
        self.screen.blit(grid.draw(),(0,0))
        for entity in entities : 
            self.screen.blit(entity.image,entity.px_loc)
        self.screen.blit(cross_hair(),(CENTER[0]-5,CENTER[1]-5))
        pygame.display.flip() 
   
def cross_hair() : 
    image = pygame.Surface((11,11))
    image.set_colorkey((255,255,255))
    image.fill((254,254,254))
    #pointlist = [(1,1),(10,10)]
    #pygame.draw.line(image,(254,254,254),False,pointlist)
    #pointlist = [(10,10),(1,1)]
    #pygame.draw.line(image,(254,254,254),False,pointlist)
    return image
   


class GameState():
    def __init__(self):
        self.focus = [0,0]
        self.zoom  = 10 # Meters/Pixel
        self.image = Image() 
        self.grid  = Grid(self.zoom,self.focus)
        self.entities = self.init_entities()
        self.image.init(self.grid, self.entities) 
        
    def init_entities(self) : 
        ent_arr = []
        #ent_arr.append(Planet(radius=100,coor=(0,0),velocity=(1,1)))
        #ent_arr.append(Planet(radius=100,coor=(1000,1000),velocity=(-1,-1)))
        #vel = np.sqrt(500*10*G/2000)/2
        #ent_arr.append(Planet(radius=500,coor=(-2000,0),velocity=(0,vel)))
        #ent_arr.append(Planet(radius=500,coor=(2000,0),velocity=(0,-vel)))
        #vel = np.sqrt(300*10*G/2000)/2
        #ent_arr.append(Planet(radius=500,coor=(10000,1000),velocity=(0,vel)))
        #ent_arr.append(Planet(radius=500,coor=(14000,1000),velocity=(0,-vel)))
    
        sun_radius = 2000
        sun_density = 100
        sun_mass = sun_radius*sun_density
        ss_rad = 50000
      
        ent_arr.append(Planet(radius=sun_radius,coor=[0,0],density=sun_density))
        for i in range(50) : 
            x_coor = rand.randint(-ss_rad,ss_rad)
            y_coor = rand.randint(-ss_rad,ss_rad) 
            theta = np.abs(np.arctan(y_coor/x_coor))
            vel = np.sqrt(sun_mass*G/distance([0,0],[x_coor,y_coor]))
            vel_x = np.cos(theta)*vel*np.sign(-y_coor)
            vel_y = np.sin(theta)*vel*np.sign(x_coor)
            ent_arr.append(Planet(coor=(x_coor,y_coor),velocity=[vel_x,vel_y],density=0.01))

        #ent_arr.append(Planet(radius=1000,coor=[0,0],density=10))
        #vel = np.sqrt(1000*10*G/2000)
        #ent_arr.append(Planet(radius=100,coor=[2000,0],velocity=(0,-vel),density=0.001))
        #vel = np.sqrt(1000*10*G/6000)
        #ent_arr.append(Planet(radius=200,coor=[6000,0],velocity=(0,-vel),density=0.001))
        
        return ent_arr
    
    def scroll(self, direction) : 
        if direction : # Zoom out
            self.zoom += 1
        else : 
            if self.zoom > 1 : 
                self.zoom -= 1
        self.grid.update(self.zoom,self.focus)
        for entity in self.entities : 
            entity.zoom(self.zoom,self.focus)

    def move(self, direction) :  
        if   direction == 273 : self.focus[1] += self.zoom*10 # UP
        elif direction == 274 : self.focus[1] -= self.zoom*10 # DOWN 
        elif direction == 275 : self.focus[0] += self.zoom*10 # RIGHT 
        elif direction == 276 : self.focus[0] -= self.zoom*10 # LEFT
        self.grid.update(self.zoom,self.focus)
        for entity in self.entities : 
            entity.move(self.zoom,self.focus)
       

    def merge(self, e1, e2) : 
        mass = e1.mass + e2.mass
        radius = np.sqrt(e1.radius**2 + e2.radius**2)
        velocity =    [(e1.velocity[0]*e1.mass + e2.velocity[0]*e2.mass)/mass,\
                       (e1.velocity[1]*e1.mass + e2.velocity[1]*e2.mass)/mass]
        e3 = e1
        e3.mass = mass
        e3.radius = radius
        e3.velocity = velocity
        e3.zoom(self.zoom, self.focus)
        return e3

    def physics(self, dt) : 

        for entity in self.entities : 
            # Check collision
            for e in self.entities : 
                if e != entity: # don't calculate self collision
                    if distance(entity.coor,e.coor) < (entity.radius + e.radius)/4*3 : 
                        entity = self.merge(entity, e)
                        self.entities.remove(e)

        for entity in self.entities : 
            forces = np.zeros([1,2])
            m1 = entity.mass
            for e in self.entities :  # Make a list of objects acting on an entity
                if e != entity: # don't calculate force for itself
                    m2 = e.mass
                    [dy,dx] = [entity.coor[1]-e.coor[1],entity.coor[0]-e.coor[0]]
                    if dx != 0 : 
                        theta = np.abs(np.arctan(dy/dx))
                    else : 
                        theta = np.pi/2
                    r2 = distance2(entity.coor,e.coor)
                    F = G*m1*m2/r2
                    Fx = F*np.cos(theta)*np.sign(-dx)
                    Fy = F*np.sin(theta)*np.sign(-dy)
                    forces = np.append(forces,[[Fx,Fy]],axis=0)
            entity.forces = forces 
            entity.physics(dt,self.zoom,self.focus)
            #print(np.sum(forces,axis=0),'v= ', entity.velocity, 'a= ', entity.accel, end=' | ')
        #print('----')

    def entity_clicked(self, pos) : 
        idx = 0
        for e in self.entities : 
            if distance(pos,e.coor) < e.radius : 
                return idx 
            idx += 1
        return None
         

def force_calc(m1,m2,r) : 
    return G*m1*m2/r**2
def distance(a,b):
    return np.sqrt((a[1]-b[1])**2+(a[0]-b[0])**2)
def distance2(a,b):
    return (a[1]-b[1])**2+(a[0]-b[0])**2

def mouse_loc(pos,focus,zoom) : # Mouses pixel location to gamestate coordinates 
    return [ int((pos[0]+focus[0]/zoom-CENTER[0])*zoom),\
             int((pos[1]-focus[1]/zoom-CENTER[1])*-zoom) ] 

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

    time = 0
    graphics_time = 0
    # define a variable to control the main loop
    running = True
    toggle_grid = False
    pause_physics = True
    track_entity = None 
     
    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        time = pygame.time.get_ticks() 
        if time-graphics_time > 20 :
            if pause_physics == False : 
                gamestate.physics(time-graphics_time)
            if track_entity != None : 
                gamestate.focus = gamestate.entities[track_entity].coor
                gamestate.move(0)
            gamestate.image.update(gamestate.grid,gamestate.entities,gamestate.focus)
            graphics_time = time

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN : 
                if event.button == 1 : 
                    mouse_coor = mouse_loc(event.pos,gamestate.focus,gamestate.zoom)
                    track_entity = gamestate.entity_clicked(mouse_coor) 
                    print(mouse_coor, track_entity)
                    if track_entity is None : 
                        gamestate.focus = mouse_loc(event.pos,gamestate.focus,gamestate.zoom)
                        gamestate.move(0)
                if event.button == 4 : gamestate.scroll(0) # Zoom in
                if event.button == 5 : gamestate.scroll(1) # Zoom out
            elif event.type == pygame.KEYDOWN : 
                if track_entity == None : 
                    if event.key >= 273 and event.key <= 276 : gamestate.move(event.key)
                if event.key == 32 : pause_physics = not pause_physics  #Space bar to pause physics
                #if event.key == 32 : 
                #    gamestate.physics(10)  #Space bar to pause physics
                #    for e in gamestate.entities : 
                #        print(e.velocity, end=' | ')
                #    print()
                if event.key == 27 : track_entity = None 
                if event.key == 103 : toggle_grid = not toggle_grid
            #elif event.type == pygame.MOUSEMOTION : 
            #    print(mouse_loc(event.pos, gamestate.focus, gamestate.zoom))
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

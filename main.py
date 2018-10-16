# import the pygame module, so you can use it
import pygame
import numpy as np
import random as rand
from logo import draw_logo
from entities import Body
from entities import Grid

#SCREEN_SIZE = (960,540)
SCREEN_SIZE = (1440,810)
#SCREEN_SIZE = (1920,1080)
CENTER = (int(SCREEN_SIZE[0]/2),int(SCREEN_SIZE[1]/2))
FPS = 30
FRAME_DELAY = 1/FPS*1000
WHITE = 0xFFFFFF 
BLACK = 0x000000
G = 5 

class Image(): 
    def __init__(self) : 
        self.time = 0
        self.focus = [0,0]       
        self.zoom  = 10 # Meters/Pixel
        self.tracking = None
        self.grid  = Grid(self.zoom, self.focus)
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
    
    def init(self,entities) : 
        if self.grid.grid_enable : self.screen.blit(self.grid.draw(),(0,0))
        else : self.screen.fill((20,20,20))
        for e in entities : 
            e.draw(self.zoom,self.focus)
            if(e.visible) : 
                self.screen.blit(e.image,e.px_ul)
        pygame.display.flip() 

        
    def update(self,entities) : 
        if self.grid.grid_enable : self.screen.blit(self.grid.draw(),(0,0))
        else : self.screen.fill((20,20,20))
        for e in entities : 
            e.draw(self.zoom,self.focus)
            if(e.visible) : 
                self.screen.blit(e.image,e.px_ul)
        self.screen.blit(cross_hair(),(CENTER[0]-5,CENTER[1]-5))
        pygame.display.flip() 
    
    def scroll(self, direction, entities) : 
        if direction : # Zoom out
            if self.zoom < 50 : 
                self.zoom += 1
            else : 
                self.zoom += 5
        else : 
            if self.zoom > 1 : 
                if self.zoom < 50 : 
                    self.zoom -= 1
                else : 
                    self.zoom -= 5
        if self.grid.grid_enable : self.grid.update(self.zoom,self.focus)
        for e in entities : 
            e.draw(self.zoom,self.focus)
    
    def move(self, direction, entities) :  
        if   direction == 273 : self.focus[1] += self.zoom*10 # UP
        elif direction == 274 : self.focus[1] -= self.zoom*10 # DOWN 
        elif direction == 275 : self.focus[0] += self.zoom*10 # RIGHT 
        elif direction == 276 : self.focus[0] -= self.zoom*10 # LEFT
        if self.grid.grid_enable : self.grid.update(self.zoom,self.focus)
        for e in entities : 
            e.move(self.zoom,self.focus)

    def set_focus(self, entities, coor = None) : 
        if coor is None : 
            if self.tracking : 
                idx = self.tracking_idx(entities)
                #track_list = []
                #for e in entities : 
                #    track_list.append(e.id)
                #if self.tracking in track_list : 
                #    self.focus = entities[track_list.index(self.tracking)].coor
                if idx is not None: 
                    self.focus = entities[idx].coor
        else : 
            self.focus = coor
        self.move(0,entities)

    def mouse_loc(self,pos) : # Mouses pixel location to gamestate coordinates 
        return [ int((pos[0]+self.focus[0]/self.zoom-CENTER[0])*self.zoom),\
                 int((pos[1]-self.focus[1]/self.zoom-CENTER[1])*-self.zoom) ] 

    def track_entity(self, pos, entities) : 
        mouse_coor = self.mouse_loc(pos)
        self.tracking = None
        for e in entities : 
            if distance(mouse_coor,e.coor) < e.radius : 
                self.tracking = e.id 

        if self.tracking :
            idx = self.tracking_idx(entities) 
            print('planet= ', self.tracking, ' collisions = ', entities[idx].collisions,\
                  'mass = ' , entities[idx].mass, 'radius = ', entities[idx].radius) 
    
    def tracking_idx(self, entities) : 
        track_list = []
        for e in entities : 
            track_list.append(e.id)
        if self.tracking in track_list : 
            return track_list.index(self.tracking)
        return None

def cross_hair() : 
    image = pygame.Surface((11,11))
    image.set_colorkey((255,255,255))
    image.fill((254,254,254))
    return image
   


class GameState():
    def __init__(self):
        self.speed = FRAME_DELAY
        self.pause = True
        self.image = Image() 
        self.entities = self.init_entities()
        self.image.init(self.entities) 
        
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
    
        sun_radius = 10000
        sun_density = 5 
        sun_mass = sun_radius*sun_density
        ss_rad = 75000
      
        ent_arr.append(Body(radius=sun_radius,coor=[0,0],density=sun_density))
        for i in range(50) : 
            x_coor = rand.randint(-ss_rad,ss_rad)
            y_coor = rand.randint(-ss_rad,ss_rad) 
            theta = np.abs(np.arctan(y_coor/x_coor))
            vel = np.sqrt(sun_mass*G/distance([0,0],[x_coor,y_coor]))
            vel_x = np.cos(theta)*vel*np.sign(-y_coor)
            vel_y = np.sin(theta)*vel*np.sign(x_coor)
            ent_arr.append(Body(coor=(x_coor,y_coor),velocity=[vel_x,vel_y],density=1))

        #ent_arr.append(Planet(radius=1000,coor=[0,0],density=10))
        #vel = np.sqrt(1000*10*G/2000)
        #ent_arr.append(Planet(radius=100,coor=[2000,0],velocity=(0,-vel),density=0.001))
        #vel = np.sqrt(1000*10*G/6000)
        #ent_arr.append(Planet(radius=200,coor=[6000,0],velocity=(0,-vel),density=0.001))
        
        return ent_arr
    
    def merge(self, e1, e2) : 
        mass = e1.mass + e2.mass
        radius = np.sqrt(e1.radius**2 + e2.radius**2)
        velocity =    [(e1.velocity[0]*e1.mass + e2.velocity[0]*e2.mass)/mass,\
                       (e1.velocity[1]*e1.mass + e2.velocity[1]*e2.mass)/mass]
        e3 = e1
        e3.mass = mass
        e3.radius = radius
        e3.velocity = velocity
        e3.collisions = e1.collisions + e2.collisions + 1
        #e3.draw(self.image.zoom, self.image.focus)
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
            entity.physics(dt,self.image.zoom,self.image.focus)
            #print(np.sum(forces,axis=0),'v= ', entity.velocity, 'a= ', entity.accel, end=' | ')
        #print('----')

         
    def print_stats(self) : 
        print('bodies = ', len(self.entities))

def distance(a,b):
    return np.sqrt((a[1]-b[1])**2+(a[0]-b[0])**2)

def distance2(a,b):
    return (a[1]-b[1])**2+(a[0]-b[0])**2


# define a main function
def main():
     
    pygame.init()

    logo = draw_logo()
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")
     
    gs = GameState()

    time = 0

    running = True
     
    # main loop
    while running:

        # Things that run on time
        time = pygame.time.get_ticks() 
        if time-gs.image.time > FRAME_DELAY :
            if gs.pause == False : 
                gs.physics(gs.speed)
            if gs.image.tracking != None : 
                gs.image.set_focus(gs.entities) 
            gs.image.update(gs.entities)
            gs.image.time = time

        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN : 
                if event.button == 1 : 
                    gs.image.track_entity(event.pos,gs.entities)
                    if gs.image.tracking is None : 
                        gs.image.set_focus(gs.entities,gs.image.mouse_loc(event.pos))
                if event.button == 4 : gs.image.scroll(0,gs.entities) # Zoom in
                if event.button == 5 : gs.image.scroll(1,gs.entities) # Zoom out
            elif event.type == pygame.KEYDOWN : 
                if gs.image.tracking == None : 
                    if event.key >= 273 and event.key <= 276 : gs.image.move(event.key,gs.entities)
                if event.key == 32 : gs.pause = not gs.pause  #Space bar to pause physics
                #if event.key == 32 : 
                #    gamestate.physics(10)  #Space bar to pause physics
                #    for e in gamestate.entities : 
                #        print(e.velocity, end=' | ')
                #    print()
                if event.key == 27 : gs.image.tracking = None  # Esc to cancel tracking
                if event.key == 103 :  # G to toggle grid
                    gs.image.grid.grid_enable = not gs.image.grid.grid_enable 
                if event.key == 44 : gs.speed /= 2 #  < decrease speed
                if event.key == 46 : gs.speed *= 2 #  < increase speed
                if event.key == 47 : gs.speed = FRAME_DELAY  # / realtime
                if event.key == 118  : gs.print_stats() # V to print stats
                    
            #elif event.type == pygame.MOUSEMOTION : 
            #    print(gs.image.mouse_loc(event.pos))
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

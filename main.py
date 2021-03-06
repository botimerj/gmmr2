# import the pygame module, so you can use it
import pygame
import numpy as np
import random as rand
import config 
import solar_system
from logo import draw_logo
from entities import Body
from entities import Grid

class Image(): 
    def __init__(self) : 
        self.display = True
        self.time = 0
        self.focus = [0,0]       
        self.zoom  = 1 # Meters/Pixel
        self.tracking = None
        self.grid  = Grid(self.zoom, self.focus)
        self.screen = pygame.display.set_mode(config.SCREEN_SIZE)
    
    def init(self,entities) : 
        self.zoom_full(entities)
        self.zoom_full(entities)

    # Updates the images of all elements (redraws each shape: expensive)
    def update(self,entities) :     
        for e in entities : 
            e.draw(self.zoom,self.focus)
            e.physics(0,self.zoom,self.focus)

    # Redraws the screen by blitting images from entities (uses existing images: cheap)
    def draw(self,entities) : 
        if self.grid.grid_enable : self.screen.blit(self.grid.draw(),(0,0))
        else : self.screen.fill((20,20,20))
        for e in entities : 
            if(e.visible) : 
                self.screen.blit(e.image,e.px_ul)
        self.screen.blit(cross_hair(),(config.CENTER[0]-2,config.CENTER[1]-2))
        pygame.display.flip() 

    # Update the entities images to account for screen movement (does not draw anything, unless entity is bigger than the screen)
    def move(self, direction, entities) :  
        if   direction == 273 : self.focus[1] += self.zoom*10 # UP
        elif direction == 274 : self.focus[1] -= self.zoom*10 # DOWN 
        elif direction == 275 : self.focus[0] += self.zoom*10 # RIGHT 
        elif direction == 276 : self.focus[0] -= self.zoom*10 # LEFT
        if self.grid.grid_enable : self.grid.update(self.zoom,self.focus)
        for e in entities : 
            e.move(self.zoom,self.focus)

    def scroll(self, direction, entities) : 
        if direction : # Zoom out
            zoom_mod = 10**(np.ceil(np.log10(self.zoom+0.1))-1)/2
            self.zoom += zoom_mod 
        else : 
            zoom_mod = 10**(np.ceil(np.log10(self.zoom))-1)/2
            self.zoom -= zoom_mod 
            if self.zoom < 1 : self.zoom = 1
        if self.grid.grid_enable : self.grid.update(self.zoom,self.focus)
        self.update(entities)
        self.draw(entities)

    def zoom_full(self, entities) : 
        max_coor = config.CENTER[0]
        for e in entities : 
            if distance(e.coor,(0,0)) > max_coor : 
                max_coor = distance(e.coor,(0,0))
            if e.radius > max_coor:
                max_coor = e.radius*2
        self.zoom = int(max_coor/(config.CENTER[0]-100))
        self.scroll(0,entities)
    
    def set_focus(self, entities, coor = None) : 
        if coor is None : 
            if self.tracking : 
                idx = self.tracking_idx(entities)
                if idx is not None: 
                    self.focus = entities[idx].coor
        else : 
            self.focus = coor
        self.move(0,entities)

    def mouse_loc(self,pos) : # Mouses pixel location to gamestate coordinates 
        return [ int((pos[0]+self.focus[0]/self.zoom-config.CENTER[0])*self.zoom),\
                 int((pos[1]-self.focus[1]/self.zoom-config.CENTER[1])*-self.zoom) ] 

    def track_entity(self, pos, entities) : 
        mouse_coor = self.mouse_loc(pos)
        self.tracking = None
        for e in entities : 
            if distance(mouse_coor,e.coor) < e.radius : 
                self.tracking = e.id 

        if self.tracking :
            idx = self.tracking_idx(entities) 
            print('name= ', entities[idx].name)
            print('planet= ', self.tracking)
            print('mass = ' , entities[idx].mass)
            print('radius = ', entities[idx].radius) 
            print('force_list = ', entities[idx].influences)
            print('touching_list = ', entities[idx].touching)
            print('-----')
    
    def tracking_idx(self, entities) : 
        track_list = []
        for e in entities : 
            track_list.append(e.id)
        if self.tracking in track_list : 
            return track_list.index(self.tracking)
        return None

def cross_hair() : 
    image = pygame.Surface((5,5))
    image.set_colorkey((255,255,255))
    image.fill((254,254,254))
    return image
   


class GameState():
    def __init__(self):
        self.speed = config.FRAME_DELAY
        self.pause = True
        self.image = Image() 
        self.cycle = 0
        self.time  = 0
        self.cycles_per_second = 0 

        # Approx Physics
        self.N = 10 # Number of influencers
        self.sync_cycles = 1000 # Number of cycles between synchronization
        self.sync_counter = self.sync_cycles+1 
        self.id_arr = []

        # Init objects
        self.entities = self.init_entities()
        self.image.init(self.entities) 
        
    def init_entities(self) : 
        #ent_arr = solar_system.solar_system() 
        #ent_arr = solar_system.massive_bodies() 
        #ent_arr = solar_system.small_bodies() 
        #ent_arr = solar_system.unit_test1()
        #ent_arr = solar_system.unit_test2()
        #ent_arr = solar_system.unit_test3()
        #ent_arr = solar_system.unit_test4()
        #ent_arr = solar_system.unit_test5()
        ent_arr = solar_system.unit_test6()
        for e in ent_arr: 
            self.id_arr.append(e.id)
        return ent_arr
    

    def physics(self, dt) : 
        for entity in self.entities : 
            # Check collision
            for e in self.entities : 
                if e != entity: # don't calculate self collision
                    if distance(entity.coor,e.coor) < (entity.radius + e.radius)/4*3 : 
                        entity = self.merge(entity, e)
                        self.entities.remove(e)
                        self.image.update(entities)

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
                    F = config.G*m1*m2/r2
                    Fx = F*np.cos(theta)*np.sign(-dx)
                    Fy = F*np.sin(theta)*np.sign(-dy)
                    forces = np.append(forces,[[Fx,Fy]],axis=0)
            entity.forces = forces 
            entity.physics(dt,self.image.zoom,self.image.focus)
        
            self.cycle += 1
            self.time  += dt/1000
            #print(np.sum(forces,axis=0),'v= ', entity.velocity, 'a= ', entity.accel, end=' | ')
        #print('----')

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
        return e3

    def bounce(self, e1, e2) : 
        v1 = np.array(e1.velocity)
        v2 = np.array(e2.velocity)
        x1 = np.array(e1.coor)
        x2 = np.array(e2.coor)
        m1 = e1.mass
        m2 = e2.mass
        c = 2*m2/(m1+m2)
        # if v1 and v2 are similar don't update velocity
        threshold = 0.1 
        if np.linalg.norm(v1-v2)**2 > threshold :
        # From wiki on 2-D elastic collision
            v1f = v1 - c*np.dot(v1-v2,x1-x2)/np.linalg.norm(x1-x2)**2*(x1-x2)
        else : 
            # Consider them touching
            if e2.id not in e1.touching : 
                e1.touching.append(e2.id) 
                print('name = ',e1.name, ' touching_list = ', e1.touching)
            v1f = v1 - (v1-v2)*m2/(m2+m1)

        dampening = 0.9#1#0.9
        return v1f*dampening



    def collisions(self) : 
        vbounce = []
        count = 0

        # Check collision, calculate new velocity
        for entity in self.entities : 
            vbounce.append(entity.velocity)
            new_vel = np.array([0,0])
            collided = False
            for e in self.entities : 
                #print('body: ', e.type, ' ', e.coor)
                if e != entity: # don't check self collision
                    overlap = np.round(distance(entity.coor,e.coor)-entity.radius-e.radius,3)
                    if overlap < 0 :
                        count += 1
                        collided = True 
                        new_vel = new_vel + self.bounce(entity,e) 
                    else : 
                        v1 = np.array(entity.velocity)
                        v2 = np.array(e.velocity)
                        threshold = 0.01
                        if np.linalg.norm(v1-v2)**2 > threshold or overlap > 1:
                            if e.id in entity.touching : 
                                entity.touching.remove(e.id) 
            if collided : 
                vbounce[-1] = new_vel

        # Check collision, and move bodies away from of eachother if the overlap 
        for entity in self.entities:
            for e in self.entities:
                if e != entity: # don't check self collision
                    overlap = np.round(distance(entity.coor,e.coor)-entity.radius-e.radius,3)
                    if overlap < 0 :
                        [dy,dx] = [entity.coor[1]-e.coor[1],entity.coor[0]-e.coor[0]]
                        if dx != 0 : 
                            theta = np.abs(np.arctan(dy/dx))
                        else :
                            theta = np.pi/2
                        #print('old_overlap = ', overlap)
                        overlap = overlap
                        # Move smaller entity
                        if e.radius < entity.radius : 
                            e.coor = [e.coor[0] + np.abs(overlap)*np.cos(theta)*np.sign(-dx),
                                      e.coor[1] + np.abs(overlap)*np.sin(theta)*np.sign(-dy)]
                        else : 
                            entity.coor = [entity.coor[0] + np.abs(overlap)*np.cos(theta)*np.sign(dx),
                                           entity.coor[1] + np.abs(overlap)*np.sin(theta)*np.sign(dy)]
                        #print('new_overlap = ', np.round(distance(entity.coor,e.coor)-entity.radius-e.radius,3))
                        
                    #e_bigger = entity.radius < e.radius
                    #if (distance(entity.coor,e.coor)-entity.radius < e.radius/8*7 or\
                    #    distance(entity.coor,e.coor)-e.radius < entity.radius/8*7):
                        #if (distance(entity.coor,e.coor)-entity.radius < e.radius/4*3 or\
                        #    distance(entity.coor,e.coor)-e.radius < entity.radius/4*3):
                            #move the entity away from other body

                            #self.id_arr.remove(e.id)
                            #entity = self.merge(entity, e)
                            #self.entities.remove(e)
                            #self.image.update(self.entities)
                            #self.synchronize()

        idx = 0
        for entity in self.entities : 
            entity.velocity = vbounce[idx]
            idx += 1


    def synchronize(self) : 
        # For each body, save a list of top N influencers
        for entity in self.entities : 
            forces = np.zeros(self.N)
            #influences = np.zeros(self.N,dtype=int) 
            influences = [0 for i in range(self.N)]
            m1 = entity.mass
            for e in self.entities :  # Make a list of objects acting on an entity
                if e != entity: # don't calculate force for itself
                    m2 = e.mass
                    [dy,dx] = [entity.coor[1]-e.coor[1],entity.coor[0]-e.coor[0]]
                    r2 = distance2(entity.coor,e.coor)
                    F = config.G*m1*m2/r2
                    min_idx = np.argmin(forces)
                    if F > forces[min_idx] :
                        forces[min_idx] = F
                        influences[min_idx] = e.id
            # If there are less than 10 bodies remove extra values
            while 0 in influences : 
                influences.remove(0)
            entity.influences = influences
            #print('Body ID : ', entity.id)
            #print(entity.influences)
            #print('-----')
            self.sync_counter = 0

    def approx_physics(self, dt) : 
        self.collisions()
        if self.sync_counter > self.sync_cycles : 
            self.synchronize()
        self.sync_counter += 1

        for entity in self.entities : 
            forces = np.zeros([1,2])
            m1 = entity.mass
            for i in range(len(entity.influences)) :  # Calculate the force of influences on object
                e_idx = self.id_arr.index(entity.influences[i])
                e = self.entities[e_idx]
    
                # Only calculate force if they are not considered 'touching'
                if e.id not in entity.touching : 
                    m2 = e.mass
                    [dy,dx] = [entity.coor[1]-e.coor[1],entity.coor[0]-e.coor[0]]
                    if dx != 0 : 
                        theta = np.abs(np.arctan(dy/dx))
                    else : 
                        theta = np.pi/2
                    r2 = distance2(entity.coor,e.coor)
                    F = config.G*m1*m2/r2
                    Fx = F*np.cos(theta)*np.sign(-dx)
                    Fy = F*np.sin(theta)*np.sign(-dy)
                    forces = np.append(forces,[[Fx,Fy]],axis=0)
            entity.forces = forces
            entity.physics(dt/1000,self.image.zoom,self.image.focus)
            self.cycle += 1
        self.time  += dt/1000

         
    def print_stats(self) : 
        print('bodies = ', len(self.entities))
        print('cycle  = ', self.cycle)
        print('CPS    = ', self.cycles_per_second)

        time = self.time
        year = int(np.floor(time/31536000))
        time -= year*31536000
        day  = int(np.floor(time/86400))
        time -= day*86400
        hour = int(np.floor(time/3600))
        time -= hour*3600
        minute = int(np.floor(time/60))
        time -= minute*60
        second = int(time)
        print(year,'y ', day,'d ', hour,'h ', minute,'m ', second, 's',sep="")


def distance(a,b):
    return np.sqrt((a[1]-b[1])**2+(a[0]-b[0])**2)

def distance2(a,b):
    return (a[1]-b[1])**2+(a[0]-b[0])**2


# define a main function
def main():
     
    pygame.init()

    logo = draw_logo()
    pygame.display.set_icon(logo)
    pygame.display.set_caption("gmmr2")

    pygame.key.set_repeat(200,20)
     
    gs = GameState()

    time = 0


    # Cycles per second
    time_old = 0
    cycle_old = 0
    physics_cycle_count = 0
    physics_cycles_per_frame = 1

    running = True
     
    # main loop
    while running:

        # Things that run on time
        time = pygame.time.get_ticks() 
        if time - time_old > 10000 : 
            gs.cycles_per_second = (gs.cycle-cycle_old)/10
            cycle_old = gs.cycle
            time_old = time

        if gs.image.display is False : # run physics loop as fast as possible
            if gs.pause == False : 
                #gs.physics(gs.speed)
                gs.approx_physics(gs.speed)
        elif gs.image.display and time-gs.image.time > config.FRAME_DELAY :
            if gs.pause == False : 
                #gs.physics(gs.speed)
                #gs.approx_physics(gs.speed)
                #for i in range(int(np.ceil(gs.speed/100))) : 
                for i in range(physics_cycles_per_frame) : 
                    #gs.approx_physics(gs.speed)
                    gs.approx_physics(gs.speed)
            if gs.image.tracking != None : 
                gs.image.set_focus(gs.entities) 
            gs.image.draw(gs.entities)
            gs.image.time = time
            physics_cycle_count = 0

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

                # O to toggle if display is updated
                if event.key == 111 :  
                    gs.image.display = not gs.image.display
                # P to pause physics
                if event.key == 112 : 
                    gs.pause = not gs.pause  
                    print("Physics paused : ", gs.pause)
                
                if event.key == 27 : gs.image.tracking = None  # Esc to cancel tracking
                if event.key == 103 :  # G to toggle grid
                    gs.image.grid.grid_enable = not gs.image.grid.grid_enable 
                    print('display : ', gs.image.display)
                if event.key == 44 : 
                    gs.speed /= 2 #  < decrease speed
                    print(f'speed = {gs.speed/1000:.2f}')
                if event.key == 46 : 
                    gs.speed *= 2 #  < increase speed
                    print(f'speed = {gs.speed/1000:.2f}')
                if event.key == 47 : 
                    gs.speed = config.FRAME_DELAY  # / realtime
                    print(f'speed = {gs.speed/1000:.2f}')
                if event.key == 118 : gs.print_stats() # V to print stats

                # F zooms out to show all entities
                if event.key == 102 : 
                    gs.image.set_focus(gs.entities,coor=(0,0))
                    gs.image.zoom_full(gs.entities)

                # Player Control
                if event.key == 119 : 
                    gs.entities[0].velocity[1] += np.abs(gs.entities[0].velocity[1])/10+0.01 #W
                    print('Velocity: ', gs.entities[0].velocity)
                if event.key == 97  : 
                    gs.entities[0].velocity[0] -= np.abs(gs.entities[0].velocity[0])/10+0.01 #A
                    print('Velocity: ', gs.entities[0].velocity)
                if event.key == 115 : 
                    gs.entities[0].velocity[1] -= np.abs(gs.entities[0].velocity[1])/10+0.01 #S
                    print('Velocity: ', gs.entities[0].velocity)
                if event.key == 100 : 
                    gs.entities[0].velocity[0] += np.abs(gs.entities[0].velocity[0])/10+0.01 #D
                    print('Velocity: ', gs.entities[0].velocity)
                    
 
 


                    
            #elif event.type == pygame.MOUSEMOTION : 
            #    print(gs.image.mouse_loc(event.pos))
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()

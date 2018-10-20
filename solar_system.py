from entities import Body
import numpy as np
import random as rand

def solar_system():
    G = 6.67408E-11 
    SUN_R = 695508E3
    SUN_M = 1.989E30

    EARTH_R = 6378E3
    EARTH_M = 5.972E24
    EARTH_OR = 149.6E9
    
    MOON_R = 1737E3 
    MOON_M = 7.3476E22
    MOON_OR = 384400E3


    MARS_R = 3389 
    MARS_M = 6.39E23 
    MARS_OR = 227.9E9 

    ent_arr = []

    # SUN
    ent_arr.append(Body(radius  =SUN_R,\
                        coor    =[0,0],\
                        density =SUN_M/SUN_R,\
                        color   =(255,201,14)))

    # EARTH
    EARTH_VEL = np.sqrt(SUN_M*G/EARTH_OR)
    ent_arr.append(Body(radius      =EARTH_R,\
                        coor        =[EARTH_OR,0],\
                        density     =EARTH_M/EARTH_R,\
                        velocity    =[0,EARTH_VEL],\
                        color       =(0,162,232)))

    # MOON
    MOON_VEL = EARTH_VEL + np.sqrt(EARTH_M*G/MOON_OR)
    ent_arr.append(Body(radius      =MOON_R,\
                        coor        =[MOON_OR+EARTH_OR,0],\
                        density     =MOON_M/MOON_R,\
                        velocity    =[0,MOON_VEL],\
                        color       =(162,162,163)))


    # MARS 
    MARS_VEL = np.sqrt(SUN_M*G/MARS_OR)
    ent_arr.append(Body(radius      =MARS_R,\
                        coor        =[MARS_OR,0],\
                        density     =MARS_M/MARS_R,\
                        velocity    =[0,MARS_VEL],\
                        color       =(253,41,11)))

    return ent_arr


def massive_bodies():
    ent_arr = []
    G = 6.67408E-11 
    R = 695508E3
    M = 1.9890E31 #10x sun mass

    OR = 695508E4

    VEL = np.sqrt(M*G/OR)
    ent_arr.append(Body(radius      =R,\
                        coor        =[0,0],\
                        density     =M/R,\
                        velocity    =[0,0]))

    ent_arr.append(Body(radius      =R,\
                        coor        =[OR,0],\
                        density     =M/R,\
                        velocity    =[0,VEL]))

    ent_arr.append(Body(radius      =R,\
                        coor        =[-OR,0],\
                        density     =M/R,\
                        velocity    =[0,-VEL]))

    ent_arr.append(Body(radius      =R,\
                        coor        =[5*OR/np.sqrt(2),5*OR/np.sqrt(2)],\
                        density     =M/R,\
                        velocity    =[-VEL,VEL]))
    return ent_arr

def unit_test1() : 
    ent_arr = []
    G = 1
    ent_arr.append(Body(radius=10000,coor=(0,0)))
    return ent_arr

def unit_test2() : 
    G = 1
    ent_arr = []
    radius = [2000,4000]
    density = [2,2]
    mass = [radius[0]*density[0], radius[0]*density[0]]
    center = [[0,0],[20000,2000]]
    distance = [6000,8000]
    coor = []
    coor.append([center[0][0]-distance[0],0])
    coor.append([center[0][0]+distance[0],0])
    coor.append([center[1][0]-distance[1],0])
    coor.append([center[1][0]+distance[1],0])

    vel = np.sqrt(mass[0]*density[0]*G/distance[0])/2
    ent_arr.append(Body(radius=radius[0],coor=coor[0],velocity=(0,vel)))
    ent_arr.append(Body(radius=radius[0],coor=coor[1],velocity=(0,-vel)))

    vel = np.sqrt(mass[1]*density[1]*G/distance[1])/2
    ent_arr.append(Body(radius=radius[1],coor=coor[2],velocity=(0,vel)))
    ent_arr.append(Body(radius=radius[1],coor=coor[3],velocity=(0,-vel)))
    return ent_arr
   
def small_bodies() :  
    G = 1
    ent_arr = []
    sun_radius = 1000
    sun_density = 2 
    sun_mass = sun_radius*sun_density
    ss_rad = 100000
  
    ent_arr.append(Body(radius=sun_radius,coor=[0,0],density=sun_density))
    for i in range(20) : 
        x_coor = rand.randint(-ss_rad,ss_rad)
        y_coor = rand.randint(-ss_rad,ss_rad) 
        theta = np.abs(np.arctan(y_coor/x_coor))
        vel = np.sqrt(sun_mass*G/distance([0,0],[x_coor,y_coor]))
        vel_x = np.cos(theta)*vel*np.sign(-y_coor)
        vel_y = np.sin(theta)*vel*np.sign(x_coor)
        ent_arr.append(Body(coor=(x_coor,y_coor),velocity=[vel_x,vel_y],density=1))

    #ent_arr.append(Body(radius=1000,coor=[0,0],density=10))
    #vel = np.sqrt(1000*10*G/2000)
    #ent_arr.append(Body(radius=100,coor=[2000,0],velocity=(0,-vel),density=0.001))
    #vel = np.sqrt(1000*10*G/6000)
    #ent_arr.append(Body(radius=200,coor=[6000,0],velocity=(0,-vel),density=0.001))

    return ent_arr

def distance(a,b):
    return np.sqrt((a[1]-b[1])**2+(a[0]-b[0])**2)

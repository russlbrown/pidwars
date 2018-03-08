#!/usr/bin/env python

"""Draw a cube on the screen. every frame we orbit
the camera around by a small amount and it appears
the object is spinning. note i've setup some simple
data structures here to represent a multicolored cube,
we then go through a semi-unopimized loop to draw
the cube points onto the screen. opengl does all the
hard work for us. :]
"""
#import psyco
#psyco.full()
import sys
import pygame
from pygame.locals import *

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print ('The GLCUBE example requires PyOpenGL')
    raise SystemExit

import random

#some simple data for a colored cube
#here we have the 3D point position and color
#for each corner. then we have a list of indices
#that describe each face, and a list of indieces
#that describes each edge


#BitBot Shape
bit_bot_vertices = (
        (-0.25, -0.25, 0.0),#p0: bottom front left
        (-0.25, 0.25, 0.0), #p1: bottom back left
        (0.25, 0.25, 0.0),  #p2: bottom back right
        (0.25, -0.25, 0.0), #p3: bottom front right
        (-0.25, -0.25, 1.0),#p4: top front left
        (-0.25, 0.25, 1.0), #p5: top back left
        (0.25, 0.25, 1.0),  #p6: top back right
        (0.25, -0.25, 1.0)) #p7: top front right

bit_bot_triangles = ((0,1,2),(0,2,3),
                     (0,4,7),(0,7,3),
                     (0,1,5),(0,5,4),
                     (1,5,6),(1,6,2),
                     (3,2,6),(3,6,7),
                     (4,5,6),(4,6,7))


#colors are 0-1 floating values
CUBE_COLORS = (
    (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1),
    (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)
)

CUBE_QUAD_VERTS = (
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
)

CUBE_EDGES = (
    (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7),
)

def drawcube(x,y,z,colors):
    CUBE_POINTS = (
        (x+0.25, y-0.25, z),  (x+0.25, y+0.25, z),
        (x-0.25, y+0.25, z),  (x-0.25, y-0.25, z),
        (x+0.25, y-0.25, z+1),  (x+0.25, y+0.25, z+1),
        (x-0.25, y-0.25, z+1),  (x-0.25, y+0.25, z+1)
    )

    "draw the cube"
    allpoints = list(zip(CUBE_POINTS, CUBE_COLORS))

##    glBegin(GL_QUADS)
##    for face in CUBE_QUAD_VERTS:
##        for vert in face:
##            pos, color = allpoints[vert]
##            glColor3fv(color)
##            glVertex3fv(pos)
##    glEnd()

    glColor3f(colors[0],colors[1],colors[2])
    glBegin(GL_LINES)
    for line in CUBE_EDGES:
        for vert in line:
            pos, color = allpoints[vert]
            glVertex3fv(pos)

    glEnd()

#colors are 0-1 floating values
CUBE2_COLORS = (
    (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0),
    (1, 0, 0), (1, 0, 0), (1, 0, 0), (1, 0, 0)
)

CUBE2_QUAD_VERTS = (
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
)

CUBE2_EDGES = (
    (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
    (6,3), (6,4), (6,7), (5,1), (5,4), (5,7),
)

def drawcube2(x,y,z,):
    CUBE2_POINTS = (
        (x+0.25, y-0.25, z),  (x+0.25, y+0.25, z),
        (x-0.25, y+0.25, z),  (x-0.25, y-0.25, z),
        (x+0.25, y-0.25, z+1),  (x+0.25, y+0.25, z+1),
        (x-0.25, y-0.25, z+1),  (x-0.25, y+0.25, z+1)
    )

    "draw the cube"
    allpoints = list(zip(CUBE2_POINTS, CUBE2_COLORS))

##    glBegin(GL_QUADS)
##    for face in CUBE2_QUAD_VERTS:
##        for vert in face:
##            pos, color = allpoints[vert]
##            glColor3fv(color)
##            glVertex3fv(pos)
##    glEnd()

    glColor3f(1.0, 0, 0)
    glBegin(GL_LINES)
    for line in CUBE2_EDGES:
        for vert in line:
            pos, color = allpoints[vert]
            glVertex3fv(pos)
            #print "    "
            #print pos

    glEnd()

def draw_beam(x1,y1,z1,x2,y2,z2,colors):

    glColor3f(colors[0],colors[1],colors[2])
    glBegin(GL_LINES)
    pos1, color = ((x1,y1,z1),(1,1,1))#allpoints[vert]
    glVertex3fv(pos1)
    pos2, color = ((x2,y2,z2),(1,0,0))#allpoints[vert]
    glVertex3fv(pos2)

    glEnd()

def generate_bot(team, x, y, colors):
    Kp = 0.1
    Ki = 0.0
    Kd = 0.5
    
    bot_template = {
        'is_alive' : True,
        'health' : 100,
        '3D_model' : 'cube',
        'team' : team,
        'color' : [colors[0],colors[1],colors[2]],
        'x' : x,
        'y' : y,
        'dx' : 0.0,
        'dy' : 0.0,
        'Kp' : Kp,
        'Ki' : Ki,
        'Kd' : Kd,
        'previous_error_x' : 0.0,
        'previous_error_y' : 0.0,
        'integral_x' : 0.0,
        'integral_y' : 0.0,
        'has_setpoint' : True,
        'setpoint_x' : x,
        'setpoint_y' : y, 
        'max_thrust' : 0.04,
        'nearest_enemy' : -1,
        'vec_of_nearest_enemy_x' : 0.0,
        'vec_of_nearest_enemy_y' : 0.0,
        'nearest_friend' : -1,
        'vec_of_nearest_friend_x' : 0.0,
        'vec_of_nearest_friend_y' : 0.0,
        'nearest_friend_in_combat' : -1,
        'vec_of_nearest_friend_in_combat_x' : 0.0,
        'vec_of_nearest_friend_in_combat_y' : 0.0,
        'is_retreating' : False,
        'retreat_duration' : 20,
        'time_to_start_hunting' : 80,
        'is_roaming' : False,
        'is_advancing' : False,
        'sight_range' : 10,
        'atack_range' : 7,
        'attack_damage' : 10,
        'attack_delay' : 5,
        'time_since_last_attack' : 0,
        'accuracy' : 50
        }
    return bot_template

def main():
    pygame.init()
    clock = pygame.time.Clock()
    #=======================USER EDITABLE VARRIABLES=========================
    number_of_teams = 2                 #2-6
    players_per_team = 20                #set the number of players per team
    field_length = 60
    field_width = 40 
    sight_range = 10
    dt = 1.0
    AirDragCoeff = 0.95 #max speed = max_thrust * (1/airDrag - 1)
    
    attack_range = 7.0
    attack_range_squared = 0.0

    wall_bounce = -0.9
    color_by_team = [[0.0,0.0,1.0],
                     [1.0,0.0,0.0],
                     [0.0,1.0,0.0]]
    perimeter_color = [1.0,1.0,1.0]

    #=================== VARIABLES ======================
    sight_range_squared = sight_range ** 2
    attack_range_squared = 49.0

    enemies_in_range = 0
    friends_in_range = 0
    nearest_friend = -1
    nearest_friend_in_combat = -1
    dist_of_nearest_friend_in_combat = 10000.0
    farthest_friend = -1
    dist_of_farthest_friend = 0.0
    nearest_enemy = -1
    is_retreating = False
    is_advancing = False
    dist_of_nearest_enemy = 10000.0
    dist_of_nearest_friend = 10000.0
    temp_dist = 1000.0
    thrust_squared = 0.0
    over_thrust = 0.0
    enemy_friend_ratio = 0.0
    output_x = 0.0
    output_y = 0.0
    #==================generate the bots================================
    random.seed()
    bot = []
    for i in range(players_per_team):
        for j in range(number_of_teams):
            bot.append(generate_bot(j + 1, random.uniform(0,field_length),
                                    random.uniform(0,field_width), color_by_team[j]))
            #bot.append(generate_bot(i + 1, field_length*0.4* i, j*2))
 
    #bot[19]['attack_damage'] = 50########################
    
    "run the demo"
    #initialize pygame and setup an opengl display
    pygame.init()
    screen = pygame.display.set_mode((1280,720), OPENGL|DOUBLEBUF)
    glEnable(GL_DEPTH_TEST)        #use our zbuffer
    
    #setup the camera
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0,1280/720.0,0.1,100.0)    #setup lens
    glTranslatef(-0.5 * field_length, -0.5*field_width + 5, -field_length*0.83) #move
    glRotatef(-30, 1, 0, 0)                       #orbit higher
    # note, board size 120 x 80 is the farthest that works
    #the camera settings for this are# glTranslatef(-60.0, -40.0, -100.0)

    while True:
        #check for quit'n events
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        #other events
        #reset game
        if event.type == KEYDOWN and event.key == K_RETURN:
            x = 5.0
            y = 0.0
            dx = 0.0
            dy = -0.3

        #move setpoint
        if event.type == KEYDOWN and event.key == K_UP:
            bot[19]['setpoint_y'] = bot[19]['setpoint_y'] + 5
        if event.type == KEYDOWN and event.key == K_DOWN:
            bot[19]['setpoint_y'] = bot[19]['setpoint_y'] - 5
        if event.type == KEYDOWN and event.key == K_RIGHT:
            bot[19]['setpoint_x'] = bot[19]['setpoint_x'] + 5
        if event.type == KEYDOWN and event.key == K_LEFT:
            bot[19]['setpoint_x'] = bot[19]['setpoint_x'] - 5
            bot[19]['has_setpoint'] = True
        #if event.type == pygame.MOUSEBUTTONUP:
        #    pos = pygame.mouse.get_pos()
        #    print pos

        #-------MESSAGES---------------------    
        if event.type == pygame.MOUSEBUTTONUP:
            print("              ")
            print("Time out of combat: " + str(bot[19]['time_since_last_attack']))
            print("Mouse Position: " + str(pygame.mouse.get_pos()))
            print("Friends in Range = " + str(friends_in_range))
            print('nearest friend: ' + str(nearest_friend))
            print("enemies_in_range: " + str(enemies_in_range))
            print('nearest_enemy: ' + str(nearest_enemy))

        #clear screen and move camera
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #orbit camera around by 1 degree
        #glRotatef(1, 0, 1, 0)                    

        #zoom in/out
        #if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed == 'button4':
        #    glrotatef(-1,1,0,0)
        #if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed == 'button5':
        #    glrotatef(1,1,0,0)
        
        for i in range(number_of_teams*players_per_team):
            if bot[i]['is_alive']:
                #clear temp variables
                enemies_in_range = 0
                friends_in_range = 1
                nearest_friend = -1
                farthest_friend = -1
                nearest_friend_in_combat = -1
                dist_of_nearest_friend_in_combat = 10000
                nearest_enemy = -1
                dist_of_nearest_friend = 100000
                dist_of_farthest_friend = 0
                dist_of_nearest_enemy = 100000
                is_retreating = False
                is_advancing = False
                output_x = 0
                output_y = 0
                temp_dist = 1000.0
                

                #Check if bot has died
                if bot[i]['health'] <= 0:
                    bot[i]['is_alive'] = False

                #==============CALCULATE BOTS IN RANGE=========================
                for j in range(number_of_teams*players_per_team):
                    if i!=j and bot[j]['is_alive']:
                        #if they are on the same team and the other bot is alive
                        if bot[i]['team'] == bot[j]['team']:
                            #get the distance between them (squared)
                            temp_dist = (bot[i]['x']-bot[j]['x'])**2 + (bot[i]['y']-bot[j]['y'])**2
                            #if they are within sight range increment the number of friends in range
                            if temp_dist < sight_range_squared:
                                friends_in_range = friends_in_range + 1
                            if temp_dist < dist_of_nearest_friend:
                                dist_of_nearest_friend = temp_dist
                                nearest_friend = j
                            if (temp_dist < dist_of_nearest_friend_in_combat
                                and bot[j]['nearest_enemy'] != -1):
                                dist_of_nearest_friend_in_combat = temp_dist
                                nearest_friend_in_combat = j
                            if temp_dist > dist_of_farthest_friend:
                                dist_of_farthest_friend = temp_dist
                                farthest_friend = j
                        else:
                            #get the distance between them (squared)
                            temp_dist = (bot[i]['x']-bot[j]['x'])**2 + (bot[i]['y']-bot[j]['y'])**2
                            #if they are within sight range increment the number of enemies in range
                            if temp_dist < sight_range_squared:
                                enemies_in_range = enemies_in_range + 1
                                if temp_dist < dist_of_nearest_enemy:
                                    dist_of_nearest_enemy = temp_dist
                                    nearest_enemy = j
                        bot[i]['nearest_friend'] = nearest_friend
                        bot[i]['nearest_enemy'] = nearest_enemy
                

                #=============MOVEMENT DECISIONS========================
                #Case 1: Enemies are in Range and Friends are in Range
                #If there are far more enemies than friends, move away
                #from nearest enemy
                enemy_friend_ratio = enemies_in_range/(friends_in_range)

                bot[i]['is_roaming'] = False
                if nearest_enemy != -1: #if enemies are in range
                    if enemies_in_range >= friends_in_range: #retreat
                        bot[i]['has_setpoint'] = False
                        output_x = (bot[i]['x'] - bot[nearest_enemy]['x'])*100000
                        output_y = (bot[i]['y'] - bot[nearest_enemy]['y'])*100000
                    elif enemies_in_range <= 0.66 * friends_in_range: #advance
                        bot[i]['has_setpoint'] = True
                        bot[i]['setpoint_x'] = (bot[i]['x'] 
                            + (bot[nearest_enemy]['x'] - bot[i]['x']) * 0.75)
                        bot[i]['setpoint_y'] = (bot[i]['y']
                            + (bot[nearest_enemy]['y'] - bot[i]['y']) * 0.75)
                    else: #hold position
                        bot[i]['setpoint_x'] = bot[i]['x']
                        bot[i]['setpoint_y'] = bot[i]['y']
                else: #if enemies aren't in range
                    if nearest_friend_in_combat != -1: #approach nearest friend with enemies in range
                        bot[i]['has_setpoint'] = True
                        bot[i]['setpoint_x'] = bot[nearest_friend_in_combat]['x']
                        bot[i]['setpoint_y'] = bot[nearest_friend_in_combat]['y']
                    elif bot[i]['time_since_last_attack']<bot[i]['time_to_start_hunting']:#regroup
                        if dist_of_farthest_friend > bot[i]['sight_range']:
                            bot[i]['has_setpoint'] = True
                            bot[i]['setpoint_x'] = bot[farthest_friend]['x']
                            bot[i]['setpoint_y'] = bot[farthest_friend]['y']
                        else:
                            bot[i]['has_setpoint'] = False
                    elif bot[i]['is_roaming'] == False: # start looking around
                        bot[i]['has_setpoint'] = False
                        bot[i]['is_roaming'] = True
                                     
                #
                #


                #=======MOVEMENT CONTROL================================
                if bot[i]['has_setpoint']:
                    #control the cube with a PID in x
                    error = bot[i]['setpoint_x'] - bot[i]['x']
                    bot[i]['integral_x'] = bot[i]['integral_x'] + error#*dt
                    derivative = (error - bot[i]['previous_error_x']) #/ dt
                    output_x = (bot[i]['Kp']*error + bot[i]['Ki']
                              *bot[i]['integral_x']+ bot[i]['Kd']*derivative)
                    bot[i]['previous_error_x'] = error

                    #control the cube with a PID in y
                    error = bot[i]['setpoint_y'] - bot[i]['y']
                    bot[i]['integral_y'] = bot[i]['integral_y'] + error#*dt
                    derivative = (error - bot[i]['previous_error_y']) #/ dt
                    output_y = (bot[i]['Kp']*error + bot[i]['Ki']*
                              bot[i]['integral_y'] + bot[i]['Kd']*derivative)                                
                    bot[i]['previous_error_y'] = error

                elif bot[i]['is_roaming']: #make it keep moving
                    output_x = bot[i]['dx']*10000
                    output_y = bot[i]['dy']*10000
                
                #Limit the overall thrust as per the bot's max_thrust
                thrust_squared = output_x ** 2 + output_y ** 2
                if thrust_squared > bot[i]['max_thrust']**2:
                    over_thrust = bot[i]['max_thrust']/thrust_squared**0.5
                    output_x *= over_thrust
                    output_y *= over_thrust

                if bot[i]['is_roaming']:
                    output_x *= 0.4
                    output_y *= 0.4


                #if a bot is too close to a friend, make it move away
                if dist_of_nearest_friend < 2:
                    output_x += ((bot[i]['x']-bot[nearest_friend]['x'])
                                 /dist_of_nearest_friend)*bot[i]['max_thrust']*0.1
                    output_y += ((bot[i]['y']-bot[nearest_friend]['y'])
                                 /dist_of_nearest_friend)*bot[i]['max_thrust']*0.1
                
                #new dx = (old + pid output) * wind resistance
                bot[i]['dx'] = (bot[i]['dx'] + output_x)*AirDragCoeff
                
                if bot[i]['x'] > field_length and bot[i]['dx'] > 0:
                    bot[i]['dx'] *= wall_bounce
                if bot[i]['x'] < 0 and bot[i]['dx'] < 0:
                    bot[i]['dx'] *= wall_bounce
                bot[i]['x'] = bot[i]['x'] + bot[i]['dx']
                
                #new dy = (old + pid output) * wind resistance
                bot[i]['dy'] = (bot[i]['dy'] + output_y)*AirDragCoeff
                
                if bot[i]['y'] > field_width and bot[i]['dy'] > 0:
                    bot[i]['dy'] *= wall_bounce
                if bot[i]['y'] < 0 and bot[i]['dy'] < 0:
                    bot[i]['dy'] *= wall_bounce
                bot[i]['y'] = bot[i]['y'] + bot[i]['dy']

                #========ATTACK===============================
                if (bot[i]['time_since_last_attack'] >= bot[i]['attack_delay']
                    and nearest_enemy != -1):
                    bot[i]['time_since_last_attack'] = 0
                    if random.uniform(0,100)<=bot[i]['accuracy']:
                        bot[nearest_enemy]['health'] -= bot[i]['attack_damage']
                        #Draw bullet beam
                        draw_beam(bot[i]['x'],bot[i]['y'],1,
                                  bot[nearest_enemy]['x']+bot[nearest_enemy]['dx'],
                                  bot[nearest_enemy]['y']+bot[nearest_enemy]['dy'],0.5,
                                  bot[i]['color'])#[0],bot[i]['color'][1],bot[i]['color'][2])
                        
                    #else:#the bot misses
                        #Draw bullet beam above the targets head
                        #draw_beam(bot[i]['x'],bot[i]['y'],1,
                        #          bot[nearest_enemy]['x']+bot[nearest_enemy]['dx'],
                        #          bot[nearest_enemy]['y']+bot[nearest_enemy]['dy'],2)
                        

                else: bot[i]['time_since_last_attack'] += 1
                
                    
                
                #========DRAW BOTS============================

                #draw arena
            draw_beam(-1,-1,0,-1,field_width+1,0,perimeter_color)
            draw_beam(-1,field_width+1,0,field_length+1,field_width+1,0,perimeter_color)
            draw_beam(field_length+1,field_width+1,0,field_length+1,-1,0,perimeter_color)
            draw_beam(field_length+1,-1,0,-1,-1,0,perimeter_color)
                #if bot[i]['team'] == 1:
            if bot[i]['is_alive']:
                drawcube(bot[i]['x'], bot[i]['y'], 0, bot[i]['color'])
        
        #drawcube2(bot[0][0]['setpoint_x'] +1.5, bot[0][0]['setpoint_y'] + 1.5, 0)
        #print 'x: ' + str(bot[0][0]['setpoint_x']) + " y: " + str(bot[0][0]['setpoint_y'])
        pygame.display.flip()
        pygame.time.wait(5)
        clock.tick(20)# 60 fps maximum
        pygame.display.set_caption("fps: " + str(clock.get_fps()))#copied from online

if __name__ == '__main__': main()

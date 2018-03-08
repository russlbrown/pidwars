
import sys
import pygame
from pygame.locals import *
import random
import math
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print ('The GLCUBE example requires PyOpenGL')
    raise SystemExit

#BitBot Shape
bit_bot_vertices = (
    (-0.25, -0.25, 0.0),#p0: bottom front left
    (-0.25, 0.25, 0.0), #p1: bottom back left
    (0.25, 0.25, 0.0),  #p2: bottom back right
    (0.25, -0.25, 0.0), #p3: bottom front right
    (-0.25, -0.25, 1.0),#p4: top front left
    (-0.25, 0.25, 1.0), #p5: top back left
    (0.25, 0.25, 1.0),  #p6: top back right
    (0.25, -0.25, 1.0)  #p7: top front right
    )
bit_bot_triangles = (
    (0,1,2),(0,2,3),
    (0,4,7),(0,7,3),
    (0,1,5),(0,5,4),
    (1,5,6),(1,6,2),
    (3,2,6),(3,6,7),
    (4,5,6),(4,6,7)
    )


#colors are 0-1 floating values
CUBE_COLORS = (
    (0, 0, 1), (0, 0, 1), (0, 0, 1)##, (0, 0, 1),
    ##(0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1)
)

CUBE_QUAD_VERTS = (
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
)

CUBE_EDGES = (
    (0,1), (1,2)##, (2,0), (0,3)
    ##, (2,7), (0,4),
    ##(6,3), (6,4), (6,7), (5,1), (5,4), (5,7),
)

def drawcube(x,y,z,colors):
    CUBE_POINTS = (
        (x -0.25, y     ,   z),  (x     , y     , z+1),
        (x +0.25, y     ,   z),  (x-0.25, y-0.25,   z),
        (x +0.25, y-0.25, z+1),  (x+0.25, y+0.25, z+1),
        (x -0.25, y-0.25, z+1),  (x-0.25, y+0.25, z+1)
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

def draw_beam(x1,y1,z1,x2,y2,z2,color1, color2):

    glColor3f(color1[0],color1[1],color1[2])
    glBegin(GL_LINES)
    pos1, color = ((x1,y1,z1),(1,1,1))#allpoints[vert]
    glVertex3fv(pos1)

    glColor3f(color2[0],color2[1],color2[2])
    pos2, color = ((x2,y2,z2),(1,0,0))#allpoints[vert]
    glVertex3fv(pos2)

    glEnd()

def generate_bot(team, x, y, color, beam_color1, beam_color2,
                 attack_delay, init_time_since_last_attack,
                 time_to_start_hunting):
    Kp = 0.1
    Ki = 0.0
    Kd = 0.3

    
    
    bot_template = {
        'is_alive' : True,
        'health' : 100,
        '3D_model' : 'cube',
        'team' : team,
        'color' : color,
        'beam_color1' : beam_color1,
        'beam_color2' : beam_color2,
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
        'max_thrust' : 0.01, #0.3 works nicely
        'nearest_enemy' : -1,
        'vec_of_nearest_enemy_x' : 0.0,
        'vec_of_nearest_enemy_y' : 0.0,
        'nearest_friend' : -1,
        'vec_of_nearest_friend_x' : 0.0,
        'vec_of_nearest_friend_y' : 0.0,
        'nearest_bot': 0.0,
        'farthest_friend' : -1,
        'vec_of_farthest_friend_x' : 0.0,
        'vec_of_farthest_friend_y' : 0.0,
        'nearest_friend_in_combat' : -1,
        'vec_of_nearest_friend_in_combat_x' : 0.0,
        'vec_of_nearest_friend_in_combat_y' : 0.0,
        'is_retreating' : False,
        'retreat_duration' : 20,
        'time_to_start_hunting' : time_to_start_hunting,
        'is_roaming' : False,
        'is_advancing' : False,
        'sight_range' : 10,
        'attack_range' : 7, #7 is good
        'attack_damage' : 15, #20
        'attack_delay' : attack_delay,
        'time_since_last_attack' : init_time_since_last_attack,
        'accuracy' : 50,
        'objective_location_x' : 30,
        'objective_location_y' : 20
        }
    return bot_template

def main():
    pygame.init()
    clock = pygame.time.Clock()
    random.seed()
    #=======================USER EDITABLE VARRIABLES=========================
    number_of_teams = 2     #2-6
    players_per_team = 80//number_of_teams   #set the number of players per team
    field_length = 60
    field_width = 40 
    sight_range = 10
    time_to_start_hunting = 80 #frames
    
    dt = 1.0
    AirDragCoeff = 0.94 #max speed = max_thrust * (1/airDrag - 1)
    
    attack_range = 7.0
    attack_delay = 20 #frames between attack

    wall_bounce = -1.0 #-1 means rebound with the same velocity

    red =       [1.0, 0.0, 0.0]
    light_red = [1.0, 0.4, 0.4]
    dark_red =  [0.5, 0.0, 0.0]
    orange =       [1.0, 0.4, 0.0]
    light_orange = [1.0, 0.64, 0.4]
    dark_orange =  [0.4, 0.2, 0.0]
    yellow =       [1.0, 1.0, 0.0]
    light_yellow = [1.0, 1.0, 0.4]
    dark_yellow =  [0.2, 0.2, 0.0]
    green =       [0.0, 0.8, 0.0]
    light_green = [0.4, 1.0, 0.4]
    dark_green =  [0.0, 0.1, 0.0]
    blue =       [0.3, 0.3, 1.0]
    light_blue = [0.6, 0.6, 1.0]
    dark_blue =  [0.0, 0.0, 0.7]
    purple =       [0.5, 0.0, 1.0]
    light_purple = [0.7, 0.4, 1.0]
    dark_purple =  [0.2, 0.0, 0.5]
    black = [0.0, 0.0, 0.0]
    white = [1.0, 1.0, 1.0]
    
    
    color_by_team = [red,
                     blue,
                     green,
                     orange,
                     yellow,
                     purple]
    beam_color1_by_team = [
        light_red,
        light_blue,
        light_green,
        light_orange,
        light_yellow,
        light_purple]
    beam_color2_by_team = [
        dark_red,
        dark_blue,
        dark_green,
        dark_orange,
        dark_yellow,
        dark_purple]

    start_radius = 20
    team_radius = 3
    
    
        
    perimeter_color = [0.5,0.5,0.5]
    

    #=================== VARIABLES ======================
    bot = []
    sight_range_squared = sight_range ** 2
    attack_range_squared = 49.0
    enemies_in_range = 0
    friends_in_range = 0

    nearest_bot = -1
    dist_of_nearest_bot = 10000.0
    nearest_friend = -1
    dist_of_nearest_friend = 10000.0
    nearest_friend_in_combat = -1
    dist_of_nearest_friend_in_combat = 10000.0
    farthest_friend = -1
    dist_of_farthest_friend = 0.0
    nearest_enemy = -1
    dist_of_nearest_enemy = 10000.0
    nearest_bot = -1
    dist_of_nearest_bot = 10000.0
    
    is_retreating = False
    is_advancing = False
    
    temp_dist = 1000.0
    thrust_squared = 0.0
    over_thrust = 0.0
    enemy_friend_ratio = 0.0
    output_x = 0.0
    output_y = 0.0
    temp_x = 0.0
    temp_y = 0.0

    team_start_location = []
    for i in range(number_of_teams):
        temp_x = field_length * 0.5 + math.cos(6.28/number_of_teams*(i-1)) * start_radius
        temp_y = field_width * 0.5 + math.sin(6.28/number_of_teams*(i-1)) * start_radius
        team_start_location.append( {
            'x': temp_x,
            'y': temp_y})
 
    #==================generate the bots================================
    for i in range(players_per_team):
        for j in range(number_of_teams):
            
            bot.append(
                generate_bot(
                    j + 1,
                    random.uniform(team_start_location[j]['x'] - team_radius,
                                   team_start_location[j]['x'] + team_radius),
                    random.uniform(team_start_location[j]['y'] - team_radius,
                                   team_start_location[j]['y'] + team_radius),
                    color_by_team[j],
                    beam_color1_by_team[j],
                    beam_color2_by_team[j],
                    attack_delay,
                    random.uniform(0,attack_delay),
                    time_to_start_hunting + random.uniform(0,1.0*
                                                           time_to_start_hunting))
                )
            #bot.append(generate_bot(i + 1, field_length*0.4* i, j*2))

    #initialize pygame and setup an opengl display
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
        if event.type == QUIT or (event.type == KEYDOWN and
                                  event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

        #other events
        #reset game
        if event.type == KEYDOWN and event.key == K_RETURN:
            for i in range(len(bot)):
                bot[i]['is_alive'] = True
                bot[i]['health'] = 100
                bot[i]['x'] = random.uniform((bot[i]['team']-1)*field_length/number_of_teams,
                                            (bot[i]['team'])*field_length/number_of_teams)
                bot[i]['y'] = random.uniform(0, field_width)
                bot[i]['dx'] = 0.0
                bot[i]['dy'] = 0.0

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

        #=========Get Inputs for Each Bot======================================

        
        
        for i in range(len(bot)):
            if bot[i]['is_alive']:
                #clear temp variables
                enemies_in_range = 0
                friends_in_range = 1

                nearest_bot = -1
                dist_of_nearest_bot = 10000.0
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
##                    bot[i]['is_alive'] = False
                    bot[i]['health'] = 100
                    bot[i]['x'] = random.uniform(field_length/number_of_teams * (bot[i]['team']-1),
                                                 field_length/number_of_teams * bot[i]['team'])#team_start_location[(bot[i]['team']-1)]['x']
                    bot[i]['y'] = random.uniform(0, field_width)#team_start_location[(bot[i]['team']-1)]['y']

                #==============CALCULATE BOTS IN RANGE=========================
                for j in range(len(bot)):
                    if i != j and bot[j]['is_alive']:
                        #get the distance between them (squared)
                        temp_dist = ((bot[i]['x']-bot[j]['x'])**2 +
                                    (bot[i]['y']-bot[j]['y'])**2)
                        #if they are on the same team and the other bot is alive
                        if bot[i]['team'] == bot[j]['team']:
                            #if they are within sight range increment the number of friends in range
                            if temp_dist < bot[i]['attack_range']**2:
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
                            #if they are within sight range increment the number of enemies in range
                            if temp_dist < bot[i]['attack_range']**2:
                                enemies_in_range = enemies_in_range + 1
                                if temp_dist < dist_of_nearest_enemy:
                                    dist_of_nearest_enemy = temp_dist
                                    nearest_enemy = j
                        bot[i]['nearest_friend'] = nearest_friend
                        bot[i]['nearest_enemy'] = nearest_enemy
                    #figure out what the nearest bot is
                    if dist_of_nearest_friend < dist_of_nearest_enemy:
                        nearest_bot = nearest_friend
                        dist_of_nearest_bot = dist_of_nearest_friend
                    else:
                        nearest_bot = nearest_enemy
                        dist_of_nearest_bot = dist_of_nearest_enemy
                

                #=============MOVEMENT DECISIONS========================
                #Case 1: Enemies are in Range and Friends are in Range
                #If there are far more enemies than friends, move away
                #from nearest enemy
                enemy_friend_ratio = enemies_in_range/friends_in_range

                bot[i]['is_roaming'] = False
                bot[i]['is_retreating'] = False
                if nearest_enemy != -1: #if enemies are in range
                    if enemies_in_range > friends_in_range: #retreat
                        bot[i]['has_setpoint'] = False
                        bot[i]['is_retreating'] = True
                        output_x = (bot[i]['x'] - bot[nearest_enemy]['x'])*100000
                        output_y = (bot[i]['y'] - bot[nearest_enemy]['y'])*100000
                    elif (enemies_in_range <= 1.0 * friends_in_range
                          and dist_of_nearest_enemy > (bot[i]['attack_range']/2)**2): #advance
                        bot[i]['has_setpoint'] = True
                        bot[i]['setpoint_x'] = (bot[i]['x'] 
                            + (bot[nearest_enemy]['x'] - bot[i]['x']) * 0.8)
                        bot[i]['setpoint_y'] = (bot[i]['y']
                            + (bot[nearest_enemy]['y'] - bot[i]['y']) * 0.8)
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
                        bot[i]['has_setpoint'] = True
                        bot[i]['is_roaming'] = False
                        bot[i]['setpoint_x'] = bot[i]['objective_location_x']
                        bot[i]['setpoint_y'] = bot[i]['objective_location_y']
                        
                                     
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

                if bot[i]['time_since_last_attack'] < bot[i]['attack_delay']:
                    output_x *= 0.2
                    output_y *= 0.2


                #if a bot is too close to another bot, make it move away
           
                if dist_of_nearest_bot < 2:
                    output_x += ((bot[i]['x']-bot[nearest_bot]['x'])
                                 /dist_of_nearest_bot)*bot[i]['max_thrust']*0.1
                    output_y += ((bot[i]['y']-bot[nearest_bot]['y'])
                                 /dist_of_nearest_bot)*bot[i]['max_thrust']*0.1
                
                #calculate new dx
                bot[i]['dx'] = (bot[i]['dx'] + output_x)*AirDragCoeff
                
                if bot[i]['x'] > field_length and bot[i]['dx'] > 0:
                    bot[i]['dx'] *= wall_bounce
                if bot[i]['x'] < 0 and bot[i]['dx'] < 0:
                    bot[i]['dx'] *= wall_bounce
                bot[i]['x'] = bot[i]['x'] + bot[i]['dx']
                
                #calculate new dy
                bot[i]['dy'] = (bot[i]['dy'] + output_y)*AirDragCoeff
                
                if bot[i]['y'] > field_width and bot[i]['dy'] > 0:
                    bot[i]['dy'] *= wall_bounce
                if bot[i]['y'] < 0 and bot[i]['dy'] < 0:
                    bot[i]['dy'] *= wall_bounce
                bot[i]['y'] = bot[i]['y'] + bot[i]['dy']

                #========ATTACK===============================
                bot[i]['time_since_last_attack'] += 1
                if not(bot[i]['is_retreating']): #attack if the bot isn't retreating
                    if (bot[i]['time_since_last_attack'] >= bot[i]['attack_delay']
                        and nearest_enemy != -1):
                        bot[i]['time_since_last_attack'] = 0
                        if random.uniform(0,100)<=bot[i]['accuracy']:
                            bot[nearest_enemy]['health'] -= bot[i]['attack_damage']
                            #Draw bullet beam
                            draw_beam(bot[i]['x'],bot[i]['y'],1,
                                      bot[nearest_enemy]['x']+bot[nearest_enemy]['dx'],
                                      bot[nearest_enemy]['y']+bot[nearest_enemy]['dy'],0.25,
                                      bot[i]['beam_color1'], bot[i]['beam_color2'])
                            
                        else:#the bot misses
                            #Draw bullet beam
                            draw_beam(bot[i]['x'],bot[i]['y'],1,
                                      bot[nearest_enemy]['x']+bot[nearest_enemy]['dx'],
                                      bot[nearest_enemy]['y']+bot[nearest_enemy]['dy'],0.25,
                                      perimeter_color, black)
                        
                
                
        #========DRAW BOTS============================

        #draw arena
        draw_beam(-1,-1,0,-1,field_width+1,0,perimeter_color, perimeter_color)
        draw_beam(-1,field_width+1,0,field_length+1,field_width+1,0,perimeter_color, perimeter_color)
        draw_beam(field_length+1,field_width+1,0,field_length+1,-1,0,perimeter_color, perimeter_color)
        draw_beam(field_length+1,-1,0,-1,-1,0,perimeter_color, perimeter_color)
        for i in range(len(bot)):
            if bot[i]['is_alive']:
                drawcube(bot[i]['x'], bot[i]['y'], 0, bot[i]['color'])
        
        #drawcube2(bot[0][0]['setpoint_x'] +1.5, bot[0][0]['setpoint_y'] + 1.5, 0)
        #print 'x: ' + str(bot[0][0]['setpoint_x']) + " y: " + str(bot[0][0]['setpoint_y'])
        pygame.display.flip()
        #pygame.time.wait(5)
        clock.tick(30)# 60 fps maximum
        pygame.display.set_caption("fps: " + str(clock.get_fps()))#copied from online

if __name__ == '__main__': main()

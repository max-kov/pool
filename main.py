import graphics
import physics
import time
import pygame
from os import path
import math

resolution = [1000, 500]
balls = []
window = graphics.GameWindow(1000, 500)
table_margin = 40
ball_size = 13

def table_collision(ball,ball_id,lower_x,upper_x,lower_y,upper_y):
    if ball.x + ball.size > upper_x or ball.x - ball.size < lower_x:
        if (ball.x + ball.size > upper_x and not ball.dx < 0) or (
                            ball.x - ball.size < lower_x and not ball.dx > 0):
            #if the direction of the ball if from the wall, there is no need to change the direction
            ball.set_vector(-ball.dx, ball.dy)
    if ball.y + ball.size > upper_y or ball.y - ball.size < lower_y:
        if (ball.y + ball.size > upper_y and not ball.dy < 0) or (
                            ball.y - ball.size < lower_y and not ball.dy > 0):
            ball.set_vector(ball.dx, -ball.dy)

    table_holes = [(table_margin, table_margin),
                   (window.size_x-table_margin, table_margin),
                   (table_margin, window.size_y - table_margin),
                   (window.size_x - table_margin, window.size_y - table_margin),
                   (window.size_x / 2, table_margin),
                   (window.size_x / 2, window.size_y - table_margin)]

    for hole in table_holes:
        posx,posy=hole
        if physics.distance_test(posx,posy,ball.x,ball.y,table_margin/2):
            balls.pop(ball_id)



def check_for_collision_bouncy():
        for counter1 in range(0, len(balls)):

            ball1 = balls[counter1]
            collision_list = []
            for counter2 in range(counter1, len(balls)):
                ball2 = balls[counter2]
                if not counter1 == counter2:
                    if physics.collision_test(ball1, ball2):
                        collision_list.append(counter2)

            #collided with one ball only
            if len(collision_list)<=1:
                for index,ballnum in enumerate(collision_list):
                    physics.collide_balls(ball1,balls[ballnum])
            else:
            #collided with several balls, this will only be used at the beginning of the game
                if ball1.dy<0:
                    #collidion at a positive angle
                    collision_list.reverse()
                    for index, ballnum in enumerate(collision_list):
                        physics.collide_balls(ball1, balls[ballnum])
                elif ball1.dy>0:
                    # collidion at a negative angle
                    for index, ballnum in enumerate(collision_list):
                        physics.collide_balls(ball1, balls[ballnum])
                else:
                    #angle of collision = 0
                    physics.perfect_break(ball1,balls[collision_list[0]],balls[collision_list[1]])


            table_collision(ball1,counter1,0 +table_margin, window.size_x -table_margin,
                                  0 +table_margin, window.size_y-table_margin)

def place_planet_bouncy(ball_size):
    start_pos = pygame.mouse.get_pos()

    size = 1
    # function waits while user unpresses the screen
    while pygame.mouse.get_pressed()[0]:
        pygame.event.get()
        # this draws the circle while the user still presses the button
        pygame.draw.circle(window.surface, (255, 255, 255), start_pos, ball_size)
        window.update()
        time.sleep(0.1)

    end_pos = pygame.mouse.get_pos()
    balls.append(physics.Planet(ball_size+0.1, start_pos[0], start_pos[1]))
    balls[len(balls) - 1].add_force((end_pos[0] - start_pos[0])*60/window.fps()
                                    , (end_pos[1] - start_pos[1])*60/window.fps())


def set_pool_table(ball_size, x, y, ballnum):
    sixty_degrees = math.radians(60)
    # this is used to avoid to the balls touch at all times
    sin_60 = math.sin(sixty_degrees)

    diffx = sin_60 * ball_size * 2
    diffy = 0.5 * ball_size * 4

    ballx = 0
    bally = 0

    for ball in range(ballnum):
        balls.append(physics.Planet(ball_size, x + diffx * ballx , y - 0.5 * diffy * (bally* 2 - ballx)))
        if bally==ballx:
            ballx+= 1
            bally = 0
        else:
            bally+=1

def sound_setup():
    selection_sound = pygame.mixer.Sound(path.join('resources', 'reload.ogg'))
    destruction_sound = pygame.mixer.Sound(path.join('resources', 'boom.wav'))

    return [selection_sound, destruction_sound]



if __name__ == "__main__":
    # window init
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    pygame.display.set_caption("Gravity Simulator")
    window = graphics.GameWindow(*resolution)
    # get clicked menu option
    selected = window.main_menu()
    # setup and play sounds
    sounds = sound_setup()
    sounds[0].play()
    # get events
    events = graphics.events()



    if selected == 1:
        # bouncy balls mode selected in menu
        set_pool_table(ball_size,250,resolution[1]/2,10)
        balls.append(physics.Planet(ball_size, ball_size,  resolution[1]/2))
        balls[len(balls)-1].add_force(5.0, 0)
        while not events["closed"]:
            check_for_collision_bouncy()
            window.move_all_once(balls)
            window.draw_table(table_margin)
            events = graphics.events()

            if events["clicked"]:
                place_planet_bouncy(ball_size)

    pygame.quit()

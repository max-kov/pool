import graphics
import physics
import time
import pygame
from os import path
import math

resolution = [1000, 500]
balls = []
window = graphics.GameWindow(1000, 500)

def check_if_collided(collisions_made,ball_num):
    temp=False
    for y in range(ball_num):
        for x in range(ball_num):
            if collisions_made[y][x]:
                temp=True
    return temp

def check_for_collision_bouncy():
        for counter1 in range(0, len(balls)):

            ball1 = balls[counter1]
            collision_list = []
            for counter2 in range(counter1, len(balls)):
                ball2 = balls[counter2]
                if not counter1 == counter2:
                    if physics.collision_test(ball1, ball2):
                        collision_list.append(counter2)

            if len(collision_list)<=1:
                for index,ballnum in enumerate(collision_list):
                    print(counter1, ' ', collision_list)
                    physics.collide_balls(ball1,balls[ballnum])
            else:
                if ball1.dy<0:
                    collision_list.reverse()
                    for index, ballnum in enumerate(collision_list):
                        print(counter1, ' ', collision_list)
                        physics.collide_balls(ball1, balls[ballnum])
                elif ball1.dy>0:
                    for index, ballnum in enumerate(collision_list):
                        print(counter1, ' ', collision_list)
                        physics.collide_balls(ball1, balls[ballnum])
                else:
                    physics.perfect_break(ball1,balls[collision_list[0]],balls[collision_list[1]])


            if ball1.x + ball1.size > window.size_x or ball1.x - ball1.size < 0:
                if (ball1.x + ball1.size > window.size_x and not ball1.dx < 0) or (
                                    ball1.x - ball1.size < 0 and not ball1.dx > 0):
                    ball1.set_vector(-ball1.dx, ball1.dy)
            if ball1.y + ball1.size > window.size_y or ball1.y - ball1.size < 0:
                if (ball1.y + ball1.size > window.size_y and not ball1.dy < 0) or (
                            ball1.y - ball1.size < 0 and not ball1.dy > 0):
                    ball1.set_vector(ball1.dx, -ball1.dy)

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
        ball_size = 30
        set_pool_table(ball_size,250,resolution[1]/2,10)
        balls.append(physics.Planet(ball_size, ball_size,  resolution[1]/2))
        balls[len(balls)-1].add_force(5.0, 0)
        while not events["closed"]:
            check_for_collision_bouncy()
            window.move_all_once(balls)

            events = graphics.events()

            if events["clicked"]:
                place_planet_bouncy(ball_size)

    pygame.quit()

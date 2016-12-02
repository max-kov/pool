import graphics as gfx
import physics as phsx
import time
import pygame
from os import path
import math

balls = []
window = gfx.game_window(1000, 500)

def check_for_collision_bouncy():
    for counter1 in range(0, len(balls)):

        ball1 = balls[counter1]

        for counter2 in range(counter1, len(balls)):
            ball2 = balls[counter2]
            if not counter1==counter2:
                if phsx.collision_test(ball1, ball2):
                    phsx.collide_bouncy(ball1, ball2)


        if ball1.x + ball1.size > window.size_x or ball1.x - ball1.size<0:
            if (ball1.x + ball1.size > window.size_x and not ball1.dx < 0) or (
                                        ball1.x - ball1.size < 0 and not ball1.dx > 0):
                ball1.set_vector(-ball1.dx, ball1.dy)
        if ball1.y + ball1.size > window.size_y or ball1.y - ball1.size<0:
            if (ball1.y + ball1.size > window.size_y and not ball1.dy<0) or (ball1.y - ball1.size<0 and not ball1.dy>0):
                ball1.set_vector(ball1.dx, -ball1.dy)



def place_planet_bouncy():
    start_pos = pygame.mouse.get_pos()

    size = 1
    # function waits while user unpresses the screen
    while pygame.mouse.get_pressed()[0]:
        pygame.event.get()
        # this draws the circle while the user still presses the button
        pygame.draw.circle(window.surface, (255, 255, 255), start_pos, int(size))
        window.update()
        # increases the size every 0.1 of a second
        size += 5
        time.sleep(0.1)

    end_pos = pygame.mouse.get_pos()
    balls.append(phsx.Planet(size, start_pos[0], start_pos[1]))
    balls[len(balls) - 1].set_vector(size * (end_pos[0] - start_pos[0]) / 500,
                                     size * (end_pos[1] - start_pos[1]) / 500)


def set_pool_table(ball_size,x,y,ballnum):
    diffx = math.sin(60)*ball_size
    diffy = math.cos(60)*ball_size

    for ballx in range(ballnum):
        for bally in range(ballx):
            balls.append(phsx.Planet(ball_size, x + 2*ball_size*ballx + diffx*(ballx-1), y - 2*ball_size*bally - diffy*(ballx-1)))


if __name__ == "__main__":
    selected = window.main_menu()

    selection_sound = pygame.mixer.Sound(path.join('resources', 'reload.ogg'))
    selection_sound.play()
    destruction_sound = pygame.mixer.Sound(path.join('resources', 'boom.wav'))

    events = gfx.get_events()

    if selected == 1:
        #bouncy balls mode selected in menu

        set_pool_table(10,300,300,8)

        balls.append(phsx.Planet(10, 20, 300))
        balls[len(balls)-1].add_force(22,0)

        while not events["was_closed"]:
            check_for_collision_bouncy()
            window.move_all_once(balls)

            events = gfx.get_events()

            if events["was_clicked"]:
                place_planet_bouncy()

    pygame.quit()
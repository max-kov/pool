import graphics
import physics
import time
import pygame
from os import path
import math

resolution = [1000, 500]
balls = []
window = graphics.GameWindow(1000, 500)
table_margin = 60
ball_size = 13
side_color = (200, 200, 0)
table_color = (0, 100, 0)
cue_color = (100, 100, 100)


def are_all_not_moving():
    return_value = True
    for ball in balls:
        if not (ball.dx == 0 and ball.dy == 0):
            return_value = False
            break
    return return_value


def set_cue(ball_id):
    cue_length = 300
    cue_thickness = 3

    def draw_cue(ball_id, cue_angle, displacement, color):
        ball = balls[ball_id]
        if displacement > 0:
            if displacement > 100:
                cue_displacement = 100
            else:
                cue_displacement = displacement + ball.size
        else:
            cue_displacement = ball.size
        # dy/dx = sin(a)/cos(s) = tan(a)
        cos_a = math.cos(math.radians(cue_angle))
        sin_a = math.sin(math.radians(cue_angle))
        x_constant = sin_a * cue_thickness
        y_constant = cos_a * cue_thickness

        points = [
            (ball.x + cue_displacement * cos_a + x_constant,
             ball.y + cue_displacement * sin_a - y_constant),
            (ball.x + cue_displacement * cos_a - x_constant,
             ball.y + cue_displacement * sin_a + y_constant),
            (ball.x + cue_length * cos_a + cue_displacement * cos_a - x_constant,
             ball.y + cue_length * sin_a + cue_displacement * sin_a + y_constant),
            (ball.x + cue_length * cos_a + cue_displacement * cos_a + x_constant,
             ball.y + cue_length * sin_a + cue_displacement * sin_a - y_constant)
        ]

        pygame.draw.polygon(window.surface, color, points)

        return points

    def delete_cue(ball_id, angle, displacement):
        draw_cue(ball_id, angle, displacement,
                 table_color)
        window.draw_table_sides(table_margin, side_color)
        window.draw_table_holes(table_holes, table_margin / 3)
        window.redraw_balls(balls)

    def draw_lines(ball, angle, color):
        line_dist = 5
        sin_a = math.sin(math.radians(angle))
        cos_a = math.cos(math.radians(angle))
        line_x = ball.x + ball.size * cos_a * 2
        line_y = ball.y + ball.size * sin_a * 2
        count = 1
        while (line_x > table_margin) and (line_x < window.size_x - table_margin) and \
                (line_y > table_margin) and (line_y < window.size_y - table_margin):
            pygame.draw.line(window.surface, color, (line_x, line_y),
                             (line_x + line_dist * cos_a, line_y + line_dist * sin_a))
            line_x = line_x + 2 * line_dist * cos_a
            line_y = line_y + 2 * line_dist * sin_a
            count += 1
        window.update()

    ball = balls[ball_id]
    angle = 0
    prev_angle = angle
    rect_pointlist = draw_cue(ball_id, angle, 0, (100, 100, 100))
    window.update()

    start_pos = pygame.mouse.get_pos()
    final_pos = start_pos
    displacement = 0

    done = False
    while not done:
        start_pos = pygame.mouse.get_pos()
        pygame.event.get()
        if pygame.mouse.get_pressed()[0] and physics.is_point_in_rect(rect_pointlist, start_pos):
            done = True
            final_pos = start_pos
            inital_displacement = physics.point_distance(start_pos, (ball.x, ball.y))
            prev_displacement = inital_displacement
            # cue was displaced from the cue ball
            while pygame.mouse.get_pressed()[0]:
                pygame.event.get()
                final_pos = pygame.mouse.get_pos()
                dx = ball.x - final_pos[0] - 0.1
                dy = ball.y - final_pos[1] - 0.1

                displacement = physics.point_distance(final_pos, (ball.x, ball.y))

                if dx == 0:
                    # div by zero exception
                    angle = 90
                else:
                    angle = math.degrees(math.atan(dy / dx))
                if dx > 0:
                    angle -= 180
                if not (prev_angle == angle) or not (prev_displacement == displacement):
                    delete_cue(ball_id, prev_angle, prev_displacement - ball_size - inital_displacement)
                    draw_lines(ball, prev_angle + 180, table_color)
                    rect_pointlist = draw_cue(ball_id, angle, displacement - ball_size - inital_displacement, cue_color)
                    draw_lines(ball, angle + 180, (255, 255, 255))
                    prev_angle = angle
                    prev_displacement = displacement

                window.update()
            if (displacement - ball_size - inital_displacement <= 0):
                done = False

    draw_lines(ball, prev_angle + 180, table_color)
    # small hitting animation
    prev_n = displacement
    for n in range(int(displacement), 0, -1):
        delete_cue(ball_id, angle, prev_n - ball_size - inital_displacement)
        draw_cue(ball_id, angle, n - ball_size - inital_displacement, cue_color)
        window.update()
        prev_n = n
        # time.sleep(0.5)
    delete_cue(ball_id, prev_angle, 0 - ball_size - inital_displacement)

    sin_a = math.sin(math.radians(angle))
    cos_a = math.cos(math.radians(angle))
    ball.add_force((displacement * cos_a) / -10, (displacement * sin_a) / -10)


def create_table_holes():
    table_holes = [(int(table_margin * 1), int(table_margin * 1)),
                   (int(window.size_x - table_margin * 1), int(table_margin * 1)),
                   (int(table_margin * 1), int(window.size_y - table_margin * 1)),
                   (int(window.size_x - table_margin), int(window.size_y - table_margin * 1)),
                   (int(window.size_x / 2), int(table_margin) - 5),
                   (int(window.size_x / 2), int(window.size_y - table_margin) + 5)]
    return table_holes


def table_collision(table_holes, ball, ball_id, lower_x, upper_x, lower_y, upper_y):
    def is_near_table_holes():
        window_x_mid = window.size_x / 2
        # edge holes
        if (ball.x < table_margin * 1.2 and ball.y < table_margin * 1.5) or \
                (ball.x > window.size_x - table_margin * 1.2 and ball.y > window.size_y - table_margin * 1.2) or \
                (ball.x < table_margin * 1.2 and ball.y > window.size_y - table_margin * 1.2) or \
                (ball.x > window.size_x - table_margin * 1.2 and ball.y < table_margin * 1.2):
            return True
        else:
            # midlle holes
            if (ball.x < window_x_mid + table_margin / 2 and ball.x > window_x_mid - table_margin / 2) and \
                    (ball.y > window.size_y - table_margin or ball.y < table_margin):
                return True
            else:
                return False

    def is_hitting_sides():
        if ball.x + ball.size > upper_x or ball.x - ball.size < lower_x:
            # 1st is location check
            if (ball.x + ball.size > upper_x and not ball.dx < 0) or (
                                ball.x - ball.size < lower_x and not ball.dx > 0):
                # 2nd is vector check
                # if the direction of the ball if from the wall, there is no need to change the direction
                return True
            else:
                return False
        else:
            return False

    def is_hitting_ceilings():
        if ball.y + ball.size > upper_y or ball.y - ball.size < lower_y:
            if (ball.y + ball.size > upper_y and not ball.dy < 0) or (
                                ball.y - ball.size < lower_y and not ball.dy > 0):
                return True
            else:
                return False
        else:
            return False

    was_deleted = False
    if not is_near_table_holes():
        if is_hitting_sides():
            # if the direction of the ball if from the wall, there is no need to change the direction
            ball.set_vector(-ball.dx, ball.dy)
        if is_hitting_ceilings():
            ball.set_vector(ball.dx, -ball.dy)

    for hole in table_holes:
        posx, posy = hole
        if physics.distance_test(posx, posy, ball.x, ball.y, ball_size * 1.7):
            was_deleted = True
    return was_deleted


def check_for_collision(table_holes):
    balls_to_delete = []
    for counter1 in range(0, len(balls)):
        ball1 = balls[counter1]
        collision_list = []
        for counter2 in range(counter1, len(balls)):
            ball2 = balls[counter2]
            if not counter1 == counter2:
                if physics.collision_test(ball1, ball2):
                    collision_list.append(counter2)

        # collided with one ball only
        if len(collision_list) <= 1:
            for index, ballnum in enumerate(collision_list):
                physics.collide_balls(ball1, balls[ballnum])
        else:
            # collided with several balls, this will only be used at the beginning of the game
            if ball1.dy < 0:
                # collidion at a positive angle
                collision_list.reverse()
                for index, ballnum in enumerate(collision_list):
                    physics.collide_balls(ball1, balls[ballnum])
            elif ball1.dy > 0:
                # collidion at a negative angle
                for index, ballnum in enumerate(collision_list):
                    physics.collide_balls(ball1, balls[ballnum])
            else:
                # angle of collision = 0
                physics.perfect_break(ball1, balls[collision_list[0]], balls[collision_list[1]])

        if table_collision(table_holes, ball1, counter1, 0 + table_margin, window.size_x - table_margin,
                           0 + table_margin, window.size_y - table_margin):
            balls_to_delete.append(counter1)

    for ball in balls_to_delete:
        balls[ball].destroy(table_color)
        balls.pop(ball)


def set_pool_balls(ball_size, x, y,ball_num_txt):
    sixty_degrees = math.radians(60)
    # this is used to avoid to the balls touch at all times
    sin_60 = math.sin(sixty_degrees)

    diffx = sin_60 * ball_size * 2
    diffy = 0.5 * ball_size * 4

    ballx = 0
    bally = 0

    new_balls = [physics.Planet(ball_size, 100, resolution[1] / 2, False, (255, 255, 255),0,ball_num_txt[0])]

    ball_colors = [
        (0, 200, 200),
        (0, 0, 200),
        (150, 0, 0),
        (200, 0, 200),
        (200, 0, 0),
        (50, 0, 0),
        (100, 0, 0)
    ]
    for i, color in enumerate(ball_colors):
        new_balls.append(physics.Planet(ball_size, 100, resolution[1] / 2, False, color, i + 1,ball_num_txt[i+1]))

    new_balls.append(physics.Planet(ball_size, 100, resolution[1] / 2, False, (0, 0, 0),8,ball_num_txt[i+1]))

    for i, color in enumerate(ball_colors):
        new_balls.append(physics.Planet(ball_size, 100, resolution[1] / 2, True, color, i + 9,ball_num_txt[i+1]))

    for i, ball in enumerate(new_balls):
        if not i == 0:
            ball.move_to(x + diffx * ballx, y - 0.5 * diffy * (bally * 2 - ballx))
            if bally == ballx:
                ballx += 1
                bally = 0
            else:
                bally += 1

    return new_balls


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
    # table holes
    table_holes = create_table_holes()
    # get clicked menu option
    selected = window.main_menu(table_color)
    # setup and play sounds
    sounds = sound_setup()
    sounds[0].play()
    # get events
    events = graphics.events()
    # draw table sides
    window.draw_table_sides(table_margin, side_color)

    fontObj = pygame.font.Font(pygame.font.get_default_font(), 10)
    ball_num_txt = [(fontObj.render(str(num), False, (0, 0, 0)), fontObj.size(str(num))) for num in range(16)]
    if selected == 1:
        # bouncy balls mode selected in menu
        balls = set_pool_balls(ball_size, 700, resolution[1] / 2,ball_num_txt)
        while not events["closed"]:
            check_for_collision(table_holes)
            window.draw_table_holes(table_holes, table_margin / 3)
            window.move_all_once(balls)
            events = graphics.events()

            while are_all_not_moving():
                set_cue(0)

    pygame.quit()

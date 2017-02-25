import math
import pygame
import physics


def set_cue(gameState,ball_id):
    cue_length = 300
    cue_thickness = 3

    def draw_cue(ball_id, cue_angle, displacement, color):
        # dy/dx = sin(a)/cos(s) = tan(a)
        cos_a = math.cos(math.radians(cue_angle))
        sin_a = math.sin(math.radians(cue_angle))
        x_constant = sin_a * cue_thickness
        y_constant = cos_a * cue_thickness

        points = [
            (ball.x + displacement * cos_a + x_constant,
             ball.y + displacement * sin_a - y_constant),
            (ball.x + displacement * cos_a - x_constant,
             ball.y + displacement * sin_a + y_constant),
            (ball.x + cue_length * cos_a + displacement * cos_a - x_constant,
             ball.y + cue_length * sin_a + displacement * sin_a + y_constant),
            (ball.x + cue_length * cos_a + displacement * cos_a + x_constant,
             ball.y + cue_length * sin_a + displacement * sin_a - y_constant)
        ]

        pygame.draw.polygon(gameState.canvas.surface, color, points)

        return points

    def delete_cue(ball_id, angle, displacement):
        draw_cue(ball_id, angle, displacement,
                 gameState.table_color)
        gameState.canvas.draw_table_sides(gameState)
        gameState.canvas.draw_table_holes(gameState)
        gameState.canvas.redraw_balls(gameState.balls)

    def draw_lines(ball, angle, color):
        #draws the aiming dotted lines
        line_dist = 5
        sin_a = math.sin(math.radians(angle))
        cos_a = math.cos(math.radians(angle))
        line_x = ball.x + ball.size * cos_a * 2
        line_y = ball.y + ball.size * sin_a * 2
        count = 1
        while (line_x > gameState.table_margin) and (line_x < gameState.canvas.size_x - gameState.table_margin) and \
                (line_y > gameState.table_margin) and (line_y < gameState.canvas.size_y - gameState.table_margin):
            pygame.draw.line(gameState.canvas.surface, color, (line_x, line_y),
                             (line_x + line_dist * cos_a, line_y + line_dist * sin_a))
            line_x = line_x + 2 * line_dist * cos_a
            line_y = line_y + 2 * line_dist * sin_a
            count += 1
        pygame.display.update()

    def get_cue_displacement(mouse_pos, ball, initial_distance):
        displacement = physics.point_distance(mouse_pos, (ball.x, ball.y)) - initial_distance + ball.size
        if displacement > 0:
            if displacement > 100+ball.size:
                cue_displacement = 100
            else:
                cue_displacement = displacement
        else:
            cue_displacement = ball.size

        return cue_displacement

    ball = gameState.balls[ball_id]
    angle = 0
    prev_angle = angle
    rect_pointlist = draw_cue(ball_id, angle, ball.size, (100, 100, 100))
    pygame.display.update()

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
            inital_mouse_dist = physics.point_distance(start_pos, (ball.x, ball.y))
            prev_displacement = ball.size
            # cue was displaced from the cue ball
            while pygame.mouse.get_pressed()[0]:
                pygame.event.get()
                final_pos = pygame.mouse.get_pos()
                dx = ball.x - final_pos[0] - 0.1
                dy = ball.y - final_pos[1] - 0.1

                displacement = get_cue_displacement(final_pos,ball,inital_mouse_dist)

                if dx == 0:
                    # div by zero exception
                    angle = 90
                else:
                    angle = math.degrees(math.atan(dy / dx))
                if dx > 0:
                    angle -= 180
                if not (prev_angle == angle) or not (prev_displacement == displacement):
                    delete_cue(ball_id, prev_angle, prev_displacement)
                    draw_lines(ball, prev_angle + 180, gameState.table_color)
                    rect_pointlist = draw_cue(ball_id, angle, displacement, gameState.cue_color)
                    draw_lines(ball, angle + 180, (255, 255, 255))
                    prev_angle = angle
                    prev_displacement = displacement

                pygame.display.update()
            if (displacement == ball.size):
                done = False

    draw_lines(ball, prev_angle + 180, gameState.table_color)
    # small hitting animation
    prev_n = displacement
    for n in range(int(displacement), ball.size, -1):
        delete_cue(ball_id, angle, prev_n)
        draw_cue(ball_id, angle, n, gameState.cue_color)
        pygame.display.update()
        prev_n = n
        # time.sleep(0.5)
    delete_cue(ball_id, prev_angle, gameState.ball_size)

    sin_a = math.sin(math.radians(angle))
    cos_a = math.cos(math.radians(angle))
    ball.add_force((displacement * cos_a) / -10, (displacement * sin_a) / -10)

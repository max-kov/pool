import math
import numpy as np
import pygame

import gamestate
import physics
from config import *


class Cue(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 0
        self.target_ball = target
        self.visible = True
        self.displacement = ball_radius
        self.update()

    def update(self, *args):
        sprite_centre = np.repeat([cue_length + cue_max_displacement], 2)
        self.image = pygame.Surface(2 * sprite_centre)
        # color which will be ignored
        self.image.fill((200, 200, 200))
        self.image.set_colorkey((200, 200, 200))

        if self.visible:
            sin_cos = np.array([math.sin(self.angle), math.cos(self.angle)])
            initial_coords = np.array([math.sin(self.angle + 0.5 * math.pi), math.cos(self.angle +
                                                                                      0.5 * math.pi)]) * cue_thickness
            coord_diff = sin_cos * cue_length
            rectangle_points = np.array((initial_coords, -initial_coords,
                                         -initial_coords + coord_diff, initial_coords + coord_diff))
            rectangle_points_from_circle = rectangle_points + self.displacement * sin_cos
            pygame.draw.polygon(self.image, cue_color,
                                rectangle_points_from_circle + sprite_centre)

            self.rect = self.image.get_rect()
            self.rect.center = self.target_ball.pos.tolist()
            self.points_on_screen = rectangle_points_from_circle + self.target_ball.pos

    def is_point_in_cue(self, point):
        # this algorithm splits up the rectangle into 4 triangles using the point provided
        # if the point provided is inside the triangle the sum of triangle
        # areas should be equal to that of the rectangle
        rect_sides = [cue_thickness * 2, cue_length] * 2
        triangle_sides = np.apply_along_axis(
            physics.point_distance, 1, self.points_on_screen, point)
        calc_area = np.vectorize(physics.triangle_area)
        triangle_areas = np.sum(
            calc_area(triangle_sides, np.roll(triangle_sides, -1), rect_sides))
        rect_area = rect_sides[0] * rect_sides[1]

        return rect_area + 1 >= triangle_areas

    def update_cue_displacement(self, mouse_pos, initial_mouse_dist):
        displacement = physics.point_distance(
            mouse_pos, self.target_ball.pos) - initial_mouse_dist + ball_radius
        if displacement > cue_max_displacement:
            self.displacement = cue_max_displacement
        elif displacement < ball_radius:
            self.displacement = ball_radius
        else:
            self.displacement = displacement

    def check_if_clicked(self, game_state):
        def draw_lines(target_ball, angle, color):
            cur_pos = np.copy(target_ball.pos)
            diff = np.array([math.sin(angle), math.cos(angle)])

            while resolution[1] > cur_pos[1] > 0 and resolution[0] > cur_pos[0] > 0:
                cur_pos += aiming_line_length * diff * 2
                pygame.draw.line(game_state.canvas.surface, color, cur_pos,
                                 (cur_pos + aiming_line_length * diff))

        events = gamestate.events()
        initial_mouse_pos = events["mouse_pos"]

        if self.is_point_in_cue(initial_mouse_pos):
            self.visible = True
            initial_mouse_dist = physics.point_distance(
                initial_mouse_pos, self.target_ball.pos)

            # cue was displaced from the cue ball
            while events["clicked"]:
                events = gamestate.events()
                current_mouse_pos = events["mouse_pos"]
                displacement_from_ball_to_mouse = self.target_ball.pos - current_mouse_pos
                self.update_cue_displacement(
                    current_mouse_pos, initial_mouse_dist)
                prev_angle = self.angle
                # hack to avoid div by zero
                if not displacement_from_ball_to_mouse[0] == 0:
                    self.angle = 0.5 * math.pi - math.atan(
                        displacement_from_ball_to_mouse[1] / displacement_from_ball_to_mouse[0])
                    if displacement_from_ball_to_mouse[0] > 0:
                        self.angle -= math.pi

                game_state.redraw_all(update=False)
                draw_lines(self.target_ball, prev_angle + math.pi, table_color)
                draw_lines(self.target_ball, self.angle +
                           math.pi, (255, 255, 255))
                pygame.display.flip()

            draw_lines(self.target_ball, self.angle + math.pi, table_color)

            if self.displacement > ball_radius:
                new_velocity = -(self.displacement - ball_radius - cue_safe_displacement) * cue_hit_power * \
                    np.array([math.sin(self.angle), math.cos(self.angle)])
                change_in_disp = np.hypot(*new_velocity) * 0.1

                while self.displacement - change_in_disp > ball_radius:
                    self.displacement -= change_in_disp
                    game_state.redraw_all()

                self.target_ball.add_force(new_velocity)
                self.displacement = ball_radius
                self.visible = False

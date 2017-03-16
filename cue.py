import pygame
import math
import physics
import numpy as np


class Cue(pygame.sprite.Sprite):
    def __init__(self, target, hit_power=0.8):
        pygame.sprite.Sprite.__init__(self)

        self.visible = True

        self.target_ball = target

        self.hit_power = hit_power
        self.length = 250
        self.thickness = 3
        self.color = (50, 50, 50)
        self.angle = 0
        self.max_displacement = 100
        self.displacement = self.target_ball.radius

        self.update()

    def update(self, *args):
        sprite_centre = np.repeat([self.length + self.max_displacement], 2)
        self.image = pygame.Surface(2 * sprite_centre)
        # color which will be ignored
        self.image.fill((200, 200, 200))
        self.image.set_colorkey((200, 200, 200))

        if self.visible:
            sin_cos = np.array([math.sin(self.angle),math.cos(self.angle)])

            initial_coords = np.array([math.sin(self.angle+0.5*math.pi),math.cos(self.angle+0.5*math.pi)]) * self.thickness
            coord_diff = sin_cos*self.length
            rectangle_points = np.array((initial_coords, -initial_coords, -initial_coords + coord_diff, initial_coords + coord_diff))

            rectangle_points_from_circle = rectangle_points + self.displacement * sin_cos

            pygame.draw.polygon(self.image, self.color, rectangle_points_from_circle + sprite_centre)

            self.rect = self.image.get_rect()
            self.rect.center = self.target_ball.pos.tolist()

            self.points_on_screen = rectangle_points_from_circle + self.target_ball.pos

    def is_point_in_cue(self, point):

        # this algorithm splits up the rectangle into 4 triangles using the point provided
        # if the point provided is inside the triangle the sum of triangle areas should be equal to that of the rectangle
        rect_sides = [self.thickness * 2, self.length] * 2

        triangle_sides = np.apply_along_axis(physics.point_distance, 1, self.points_on_screen, point)
        calc_area = np.vectorize(physics.triangle_area)
        triangle_areas = np.sum(calc_area(triangle_sides,np.roll(triangle_sides,-1), rect_sides))

        rect_area = rect_sides[0] * rect_sides[1]

        return rect_area >= triangle_areas

    def update_cue_displacement(self, mouse_pos, initial_mouse_dist):
        displacement = physics.point_distance(mouse_pos,self.target_ball.pos) - initial_mouse_dist + self.target_ball.radius
        if displacement > self.max_displacement:
            self.displacement = self.max_displacement
        elif displacement < self.target_ball.radius:
            self.displacement = self.target_ball.radius
        else:
            self.displacement = displacement

    def make_visible(self):
        self.visible = True

    def make_invisible(self):
        self.visible = False

    def check_if_clicked(self, game_state):
        def draw_lines(target_ball, angle, color):
            cur_pos = np.copy(target_ball.pos)
            diff = np.array([math.sin(angle), math.cos(angle)])

            line_length = 10

            while game_state.resolution[1] > cur_pos[1] > 0 and game_state.resolution[0] > cur_pos[0] > 0:
                cur_pos += line_length * diff * 2
                pygame.draw.line(game_state.canvas.surface, color, cur_pos, (cur_pos + line_length * diff))

        events = game_state.events()
        initial_mouse_pos = events["mouse_pos"]

        if self.is_point_in_cue(initial_mouse_pos):
            self.visible = 1

            initial_mouse_dist = physics.point_distance(initial_mouse_pos, self.target_ball.pos)

            # cue was displaced from the cue ball
            while events["clicked"]:
                events = game_state.events()
                final_pos = events["mouse_pos"]
                change = self.target_ball.pos - final_pos
                self.update_cue_displacement(final_pos, initial_mouse_dist)

                prev_angle = self.angle
                if not change[0] == 0:
                    # hack to avoid div by zero
                    self.angle = 0.5*math.pi - math.atan(change[1] / change[0])
                    if change[0] > 0:
                        self.angle -= math.pi

                game_state.redraw_all(update=False)
                draw_lines(self.target_ball, prev_angle + math.pi, game_state.table_color)
                draw_lines(self.target_ball, self.angle + math.pi, (255, 255, 255))
                pygame.display.flip()

            draw_lines(self.target_ball, self.angle + math.pi, game_state.table_color)

            disp_temp = self.displacement - self.target_ball.radius - 1
            if self.displacement > self.target_ball.radius:
                for cur_disp in range(int(self.displacement), self.target_ball.radius, -1):
                    self.displacement = cur_disp
                    game_state.redraw_all()
                    game_state.mark_one_frame()

                self.target_ball.add_force(-disp_temp*self.hit_power*np.array([math.sin(self.angle),math.cos(self.angle)]))
                self.make_invisible()

import itertools
import math
import numpy as np
import pygame

import ball
import cue
import graphics
import table_sprites
from config import *


class GameState:
    def __init__(self):
        def table_points_from_side_hole(hole_coords):
            forty_five_degree_cos = math.cos(math.radians(45))
            offset = np.array([
                [- 2 * forty_five_degree_cos * hole_radius - hole_radius, hole_radius],
                [- forty_five_degree_cos * hole_radius, -
                    forty_five_degree_cos * hole_radius],
                [forty_five_degree_cos * hole_radius,
                    forty_five_degree_cos * hole_radius],
                [- hole_radius, 2 * forty_five_degree_cos * hole_radius + hole_radius]
            ])

            # flips the matrix so the final matrix would have the correct
            # starting and ending points
            flip_matrix = [1, 1]
            if hole_coords[0] < resolution[0] / 2:
                flip_matrix[0] = -1
                offset = np.flipud(offset)
            if hole_coords[1] > resolution[1] / 2:
                flip_matrix[1] = -1
                offset = np.flipud(offset)

            return hole_coords + offset * flip_matrix

        def table_points_from_middle_hole(hole_coords):
            offset = np.array([
                [-hole_radius * 2, hole_radius],
                [-hole_radius, 0],
                [hole_radius, 0],
                [hole_radius * 2, hole_radius]
            ])

            if hole_coords[1] > resolution[1] / 2:
                offset *= [1, -1]
                offset = np.flipud(offset)

            return hole_coords + offset

        pygame.init()
        pygame.display.set_caption(window_caption)

        self.balls = pygame.sprite.Group()
        self.holes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.OrderedUpdates()

        self.table_sides = []
        table_side_points = np.empty((2, 2))
        # holes_x and holes_y holds the possible xs and ys table holes
        holes_x = [table_margin, resolution[0] /
                   2, resolution[0] - table_margin]
        holes_y = [table_margin, resolution[1] - table_margin]
        # next three lines are a hack to make and arrange the hole coordinates
        # in the correct sequence
        hole_coords = np.array(list(itertools.product(holes_y, holes_x)))
        hole_coords = np.fliplr(hole_coords)
        hole_coords = np.vstack((hole_coords[:3], np.flipud(hole_coords[3:])))
        for hole in hole_coords:
            self.holes.add(table_sprites.Hole(*hole))
            if hole[0] == resolution[0] / 2:
                table_side_points = np.append(table_side_points,
                                              table_points_from_middle_hole(hole),axis=0)
            else:
                table_side_points = np.append(table_side_points,
                                              table_points_from_side_hole(hole),axis=0)

        # repaces the first empty element of the array with the last element of the same array to make
        # the array start and end with the same element
        table_side_points[1] = table_side_points[-1]
        for num, point in enumerate(table_side_points[2:]):
            # this will skip lines inside the circle
            if num % 4 != 2:
                self.table_sides.append(table_sprites.TableSide(
                    [point, table_side_points[num + 1]]))

        self.canvas = graphics.Canvas()
        self.all_sprites.add(table_sprites.TableColoring(
            resolution, table_side_color, table_side_points[2:]))
        self.all_sprites.add(self.holes)

        # fps control
        self.fps_clock = pygame.time.Clock()

    def fps(self):
        return self.fps_clock.fps()

    def mark_one_frame(self):
        self.fps_clock.tick(fps_limit)

    def create_balls(self):
        for i in range(total_ball_num):
            self.balls.add(ball.Ball(i))

    def set_pool_balls(self):
        # 0.99 and 1.99 to insure that balls are touching at the start of the
        # game
        coord_shift = np.array([math.sin(math.radians(60)) * ball_radius *
                                1.99, -ball_radius * 0.99])
        counter = [0, 0]
        initial_place = ball_starting_place_ratio * resolution
        for ball in self.balls:
            if not ball.number == 0:
                ball.move_to(initial_place + coord_shift * counter)
                if counter[1] == counter[0]:
                    counter[0] += 1
                    counter[1] = -counter[0]
                else:
                    counter[1] += 2
            else:
                ball.move_to(white_ball_initial_pos)
                self.white_ball = ball

    def start_pool(self):
        self.create_balls()
        self.set_pool_balls()
        self.all_sprites.add(self.balls)

        # add cuestick
        self.cue = cue.Cue(self.white_ball)
        self.all_sprites.add(self.cue)

    def redraw_all(self, update=True):
        self.all_sprites.clear(self.canvas.surface, self.canvas.background)
        self.all_sprites.draw(self.canvas.surface)
        self.all_sprites.update()
        if update:
            pygame.display.flip()
        self.mark_one_frame()

    def all_not_moving(self):
        return_value = True
        for ball in self.balls:
            if np.count_nonzero(ball.velocity) > 0:
                return_value = False
                break
        return return_value


def events():
    closed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True

    return {"closed": closed,
            "clicked": pygame.mouse.get_pressed()[0],
            "mouse_pos": np.array(pygame.mouse.get_pos())}

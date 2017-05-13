import itertools
import math

import numpy as np
import pygame

import ball
import config
import cue
import graphics
import table_sprites


class GameState:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(config.window_caption)

        self.balls = pygame.sprite.Group()
        self.holes = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.OrderedUpdates()
        self.canvas = graphics.Canvas()

        # stores the invisible table lines which reflect the ball when it
        # touches the table side
        self.table_sides = []
        table_side_points = np.empty((1, 2))
        # holes_x and holes_y holds the possible xs and ys table holes
        # with a position ID in the second tuple field
        # so the top left hole has id 1,1
        holes_x = [(config.table_margin, 1), (config.resolution[0] /
                                              2, 2), (config.resolution[0] - config.table_margin, 3)]
        holes_y = [(config.table_margin, 1), (config.resolution[1] - config.table_margin, 2)]
        # next three lines are a hack to make and arrange the hole coordinates
        # in the correct sequence
        all_hole_positions = np.array(
            list(itertools.product(holes_y, holes_x)))
        all_hole_positions = np.fliplr(all_hole_positions)
        all_hole_positions = np.vstack(
            (all_hole_positions[:3], np.flipud(all_hole_positions[3:])))

        for hole_pos in all_hole_positions:
            self.holes.add(table_sprites.Hole(hole_pos[0][0], hole_pos[1][0]))
            # this will generate the diagonal, vertical and horizontal table
            # pieces which will reflect the ball when it hits the table sides
            # they are generated using 4x2 offset matrices (4 points around the hole)
            # with the first point of the matrix is the starting point and the
            # last point is the ending point, these 4x2 matrices are
            # concatenated together
            # also the martices must be flipped using numpy.flipud()
            # after reflecting them using 2x1 reflection matrices, otherwise
            # starting and ending points would be reversed
            if hole_pos[0][1] == 2:
                # hole_pos[0,1]=2 means x coordinate ID is 2 which means this
                # hole is in the middle
                if hole_pos[1][1] == 2:
                    offset = np.flipud(config.middle_hole_offset) * [1, -1]
                else:
                    offset = config.middle_hole_offset
                table_side_points = np.append(
                    table_side_points, [hole_pos[0][0], hole_pos[1][0]] + offset, axis=0)
            else:
                offset = config.side_hole_offset
                if hole_pos[0][1] == 1:
                    offset = np.flipud(offset) * [-1, 1]
                if hole_pos[1][1] == 2:
                    offset = np.flipud(offset) * [1, -1]
                table_side_points = np.append(table_side_points,
                                              [hole_pos[0][0], hole_pos[1][0]] + offset, axis=0)

        # deletes the 1st point in array (leftover form np.empty)
        table_side_points = np.delete(table_side_points, 0, 0)
        for num, point in enumerate(table_side_points[:-1]):
            # this will skip lines inside the circle
            if num % 4 != 1:
                self.table_sides.append(table_sprites.TableSide(
                    [point, table_side_points[num + 1]]))

        self.table_sides.append(table_sprites.TableSide(
            [table_side_points[-1], table_side_points[0]]))

        self.all_sprites.add(table_sprites.TableColoring(
            config.resolution, config.table_side_color, table_side_points))
        self.all_sprites.add(self.holes)

        self.fps_clock = pygame.time.Clock()

    def fps(self):
        return self.fps_clock.fps()

    def mark_one_frame(self):
        self.fps_clock.tick(config.fps_limit)

    def create_balls(self):
        for i in range(config.total_ball_num):
            self.balls.add(ball.Ball(i))

    def set_pool_balls(self):
        coord_shift = np.array([math.sin(math.radians(60)) * config.ball_radius *
                                2, -config.ball_radius])
        counter = [0, 0]
        initial_place = config.ball_starting_place_ratio * config.resolution
        for ball in self.balls:
            if not ball.number == 0:
                ball.move_to(initial_place + coord_shift * counter)
                if counter[1] == counter[0]:
                    counter[0] += 1
                    counter[1] = -counter[0]
                else:
                    counter[1] += 2
            else:
                ball.move_to(config.white_ball_initial_pos)
                self.white_ball = ball

    def start_pool(self):
        self.create_balls()
        self.set_pool_balls()
        self.all_sprites.add(self.balls)

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

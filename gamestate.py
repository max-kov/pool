import itertools
import math
import numpy as np
import pygame

import ball
import cue
import graphics
import table_sprites


class GameState:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pool")

        # ball constants
        self.total_ball_num = 16
        self.balls = pygame.sprite.Group()
        self.ball_size = 14
        self.friction_coeff = 0.994

        # table and canvas constants
        self.resolution = np.array([1000, 500])
        self.table_margin = 60
        self.side_color = (200, 200, 0)
        self.table_color = (0, 100, 0)

        # other constants
        self.cue_color = (100, 100, 100)
        self.hole_rad = 20

        # sprite groups
        self.holes = pygame.sprite.Group()
        self.table_sides = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.OrderedUpdates()

        # creating table holes
        holes_x = [self.table_margin, self.resolution[0] - self.table_margin, self.resolution[0] / 2]
        holes_y = [self.table_margin, self.resolution[1] - self.table_margin]
        for i, hole in enumerate(list(itertools.product(holes_x, holes_y))):
            self.holes.add(table_sprites.Hole(*hole, radius=self.hole_rad))

        forty_five_degree_cos = math.cos(math.radians(45))
        table_side_points = [
            [self.resolution[0] / 2 - self.hole_rad * 2, self.table_margin + self.hole_rad],
            [self.resolution[0] / 2 - self.hole_rad, self.table_margin],
            [self.resolution[0] / 2 + self.hole_rad, self.table_margin],
            [self.resolution[0] / 2 + self.hole_rad * 2, self.table_margin + self.hole_rad],

            [self.resolution[0] - self.table_margin - 2 * forty_five_degree_cos * self.hole_rad - self.hole_rad,
             self.table_margin + self.hole_rad],
            [self.resolution[0] - self.table_margin - forty_five_degree_cos * self.hole_rad,
             self.table_margin - forty_five_degree_cos * self.hole_rad],
            [self.resolution[0] - self.table_margin + forty_five_degree_cos * self.hole_rad,
             self.table_margin + forty_five_degree_cos * self.hole_rad],
            [self.resolution[0] - self.table_margin - self.hole_rad,
             self.table_margin + 2 * forty_five_degree_cos * self.hole_rad + self.hole_rad],

            [self.resolution[0] - self.table_margin - self.hole_rad,
             self.resolution[1] - self.table_margin - 2 * forty_five_degree_cos * self.hole_rad - self.hole_rad],
            [self.resolution[0] - self.table_margin + forty_five_degree_cos * self.hole_rad,
             self.resolution[1] - self.table_margin - forty_five_degree_cos * self.hole_rad],
            [self.resolution[0] - self.table_margin - forty_five_degree_cos * self.hole_rad,
             self.resolution[1] - self.table_margin + forty_five_degree_cos * self.hole_rad],
            [self.resolution[0] - self.table_margin - 2 * forty_five_degree_cos * self.hole_rad - self.hole_rad,
             self.resolution[1] - self.table_margin - self.hole_rad],

            [self.resolution[0] / 2 + self.hole_rad * 2,
             self.resolution[1] - self.table_margin - self.hole_rad],
            [self.resolution[0] / 2 + self.hole_rad, self.resolution[1] - self.table_margin],
            [self.resolution[0] / 2 - self.hole_rad, self.resolution[1] - self.table_margin],
            [self.resolution[0] / 2 - self.hole_rad * 2, self.resolution[1] - self.table_margin - self.hole_rad],

            [self.table_margin + 2 * forty_five_degree_cos * self.hole_rad + self.hole_rad,
             self.resolution[1] - self.table_margin - self.hole_rad],
            [self.table_margin + forty_five_degree_cos * self.hole_rad,
             self.resolution[1] - self.table_margin + forty_five_degree_cos * self.hole_rad],
            [self.table_margin - forty_five_degree_cos * self.hole_rad,
             self.resolution[1] - self.table_margin - forty_five_degree_cos * self.hole_rad],
            [self.table_margin + self.hole_rad,
             self.resolution[1] - self.table_margin - 2 * forty_five_degree_cos * self.hole_rad - self.hole_rad],

            [self.table_margin + self.hole_rad,
             self.table_margin + 2 * forty_five_degree_cos * self.hole_rad + self.hole_rad],
            [self.table_margin - forty_five_degree_cos * self.hole_rad,
             self.table_margin + forty_five_degree_cos * self.hole_rad],
            [self.table_margin + forty_five_degree_cos * self.hole_rad,
             self.table_margin - forty_five_degree_cos * self.hole_rad],
            [self.table_margin + 2 * forty_five_degree_cos * self.hole_rad + self.hole_rad,
             self.table_margin + self.hole_rad],
            [self.resolution[0] / 2 - self.hole_rad * 2, self.table_margin + self.hole_rad],
            [self.resolution[0] / 2 - self.hole_rad, self.table_margin]
        ]

        for num, point in enumerate(table_side_points[:-1]):
            self.table_sides.add(
                table_sprites.TableSide(self.side_color, [point, table_side_points[num + 1]]))

        self.all_sprites.add(self.holes)
        self.all_sprites.add(self.table_sides)

        self.canvas = graphics.Canvas(*self.resolution, background_color=self.table_color)

        # fps control
        self.fps_clock = pygame.time.Clock()
        self.fps_limit = 200

    def fps(self):
        return self.fps_clock.fps()

    def mark_one_frame(self):
        self.fps_clock.tick(self.fps_limit)

    def create_balls(self):
        for i in range(self.total_ball_num):
            self.balls.add(ball.Ball(i, self.ball_size, self.friction_coeff))

    def set_pool_balls(self, inital_place):
        coord_shift = np.array([math.sin(math.radians(60)) * self.ball_size * 2, -self.ball_size])
        counter = [0, 0]

        for ball in self.balls:
            if not ball.number == 0:
                ball.move_to(inital_place + coord_shift * counter)
                if counter[1] == counter[0]:
                    counter[0] += 1
                    counter[1] = -counter[0]
                else:
                    counter[1] += 2
            else:
                ball.move_to([0.3, 0.5] * self.resolution)
                self.zero_ball = ball

    def start_pool(self):
        self.create_balls()
        self.set_pool_balls(self.resolution * [3.0 / 4, 0.5])
        self.all_sprites.add(self.balls)

        # add cuestick
        self.cue = cue.Cue(self.zero_ball)
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

    def events(self):
        closed = False

        for event in pygame.event.get():
            if event.type in [pygame.QUIT, pygame.KEYDOWN]:
                closed = True

        return {"closed": closed,
                "clicked": pygame.mouse.get_pressed()[0],
                "mouse_pos": np.array(pygame.mouse.get_pos())}

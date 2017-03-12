import graphics
import ballinfo
import math
import pygame
import itertools
import ball
import table_sprites
import cue
import numpy as np


class GameState:
    def __init__(self):
        def create_holes(self):
            # stores all possible xs and yss
            holes_x = [self.table_margin, self.resolution[0] - self.table_margin, self.resolution[0] / 2]
            holes_y = [self.table_margin, self.resolution[1] - self.table_margin]
            # generates hole locations
            for i, hole in enumerate(list(itertools.product(holes_x, holes_y))):
                self.holes.add(table_sprites.Hole(*hole, radius=self.hole_rad))

        def create_table_sides(self):
            sides = [[(0, 0, self.resolution[0], self.table_margin), False, False],
                     [(self.resolution[0] - self.table_margin, 0, self.resolution[0], self.resolution[1]), True, True],
                     [(0, self.resolution[1] - self.table_margin, self.resolution[0], self.resolution[1]), False, True],
                     [(0, 0, self.table_margin, self.resolution[1]), True, False]
                     ]

            for i, side in enumerate(sides):
                self.sides.add(table_sprites.TableSide(self.side_color, *side))

        pygame.init()
        pygame.display.set_caption("Gravity Simulator")

        # ball constants
        self.total_ball_num = 16
        self.balls = pygame.sprite.Group()
        self.ball_size = 13
        self.friction_coeff = 0.995

        # table and canvas constants
        self.resolution = [1000, 500]
        self.table_margin = 60
        self.side_color = (200, 200, 0)
        self.table_color = (0, 100, 0)

        # other constants
        self.cue_color = (100, 100, 100)
        self.hole_rad = 18
        self.cue_hit_power = 0.8

        # sprite groups
        self.holes = pygame.sprite.Group()
        self.sides = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.OrderedUpdates()

        create_holes(self)
        create_table_sides(self)

        self.all_sprites.add(self.sides)
        self.all_sprites.add(self.holes)

        self.canvas = graphics.Canvas(*self.resolution, background_color=self.table_color)

        # fps control
        self.fps_clock = pygame.time.Clock()
        self.fps_limit = 100

    def get_fps(self):
        return self.fps_clock.get_fps()

    def mark_one_frame(self):
        self.fps_clock.tick(self.fps_limit)

    def create_balls(self):
        for i in range(self.total_ball_num):
            self.balls.add(ball.Ball(ballinfo.BallInfo(i)))

    def set_pool_balls(self, x, y):
        sin_60 = math.sin(math.radians(60))

        diffx = sin_60 * self.ball_size * 2
        diffy = 0.5 * self.ball_size * 4

        ballx = 0
        bally = 0

        for i, ball in enumerate(self.balls):
            if not ball.number == 0:
                ball.move_to(x + diffx * ballx, y - 0.5 * diffy * (bally * 2 - ballx))
                if bally == ballx:
                    ballx += 1
                    bally = 0
                else:
                    bally += 1
            else:
                ball.move_to(0.3 * self.resolution[0], self.resolution[1] / 2.0)
                self.zero_ball = ball



    def start_pool(self):
        table_y_middle = self.resolution[1] / 2.0
        table_x_quarter = 3.0 / 4 * self.resolution[0]

        self.create_balls()
        self.set_pool_balls(table_x_quarter, table_y_middle)
        self.all_sprites.add(self.balls)

        # add cuestick
        self.cue = cue.Cue(self.zero_ball, hit_power=self.cue_hit_power)
        self.all_sprites.add(self.cue)

    def redraw_all(self,update=True):
        self.all_sprites.clear(self.canvas.surface, self.canvas.background)
        self.all_sprites.draw(self.canvas.surface)
        self.all_sprites.update(self)
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

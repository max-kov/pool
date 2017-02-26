import graphics
import ballinfo
import math
import pygame
import itertools
import ball


class GameState:
    def __init__(self):
        def get_holes(self):
            # stores all possible xs and yss
            holes_x = [self.table_margin, self.resolution[0] - self.table_margin, self.resolution[0] / 2]
            holes_y = [self.table_margin, self.resolution[1] - self.table_margin]
            # generates hole locations
            return list(itertools.product(holes_x, holes_y))

        pygame.init()
        pygame.display.set_caption("Gravity Simulator")

        # ball constants
        self.balls = []
        self.ball_size = 13

        # table and canvas constants
        self.resolution = [1000, 500]
        self.table_margin = 60
        self.side_color = (200, 200, 0)
        self.table_color = (0, 100, 0)
        self.table_holes = get_holes(self)

        # other constants
        self.cue_color = (100, 100, 100)
        self.hole_rad = 13

        self.canvas = graphics.Canvas(*self.resolution)

        # fps control
        self.fps_clock = pygame.time.Clock()
        self.fps_limit = 100

    def get_fps(self):
        return self.fps_clock.get_fps()

    def mark_one_frame(self):
        self.fps_clock.tick(self.fps_limit)

    def create_balls(self):
        for i in range(self.total_ball_num):
            ball_data = ballinfo.BallInfo(i)
            self.balls.append(
                ball.Ball(ball_data.ball_size, 0, 0, ball_data.is_striped, ball_data.ball_color, i,
                          ball_data.ball_num_txt))

    def set_pool_balls(self, x, y):
        sixty_degrees = math.radians(60)
        # this is used to avoid to the balls touch at all times
        sin_60 = math.sin(sixty_degrees)

        diffx = sin_60 * self.ball_size * 2
        diffy = 0.5 * self.ball_size * 4

        ballx = 0
        bally = 0

        self.balls[0].move_to(self, 0.3 * self.resolution[0], self.resolution[1] / 2.0)

        for i, ball in enumerate(self.balls):
            if not i == 0:
                ball.move_to(self, x + diffx * ballx, y - 0.5 * diffy * (bally * 2 - ballx))
                if bally == ballx:
                    ballx += 1
                    bally = 0
                else:
                    bally += 1

    def main_menu(self):
        # checks if mouse is in a button
        def check_mouse_pos(text_starting_place, text_ending_place, spacing, button_num):
            mouse_pos = pygame.mouse.get_pos()
            return (text_starting_place[button_num][0] - spacing < mouse_pos[0] < text_ending_place[button_num][
                0] + spacing) and \
                   (text_starting_place[button_num][1] - spacing < mouse_pos[1] < text_ending_place[button_num][
                       1] + spacing)

        # draws main menu and returns all the variables needed to check button clicks
        text_starting_place, text_ending_place, spacing, buttons = self.canvas.draw_main_menu(self.table_color)

        was_clicked = False
        button_clicked = 0

        # while a button was not clicked checks if mouse is in the button and if so changes its colour
        while not was_clicked:
            pygame.display.update()
            user_events = self.events()

            for num in range(1, len(buttons)):
                if check_mouse_pos(text_starting_place, text_ending_place, spacing, num):
                    if user_events["clicked"]:
                        was_clicked = True
                        button_clicked = num
                    else:
                        self.canvas.surface.blit(buttons[num][1], text_starting_place[num])
                else:
                    self.canvas.surface.blit(buttons[num][0], text_starting_place[num])

        return button_clicked

    def start_pool(self):
        self.total_ball_num = 16

        self.canvas.draw_table_sides(self)

        table_y_middle = self.resolution[1] / 2.0
        table_x_quarter = 3.0 / 4 * self.resolution[0]

        self.create_balls()
        self.set_pool_balls(table_x_quarter, table_y_middle)

    def do_one_frame(self):
        self.canvas.draw_table_holes(self)
        for ball in self.balls:
            ball.move_once(self)
        pygame.display.update()
        self.mark_one_frame()

    def all_not_moving(self):
        return_value = True
        for ball in self.balls:
            if not (ball.dx == 0 and ball.dy == 0):
                return_value = False
                break
        return return_value

    def events(self):
        closed = False
        clicked = False
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type in [pygame.QUIT, pygame.KEYDOWN]:
                closed = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        return {"closed": closed,
                "clicked": clicked,
                "mouse_pos": mouse_pos}

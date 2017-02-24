import graphics
import physics
import math
import pygame
import collisiontests
import itertools

class GameState:
    def __init__(self):
        def get_holes(self):
            #stores all possible xs and yss
            holes_x = [self.table_margin, self.resolution[0] - self.table_margin, self.resolution[0] / 2]
            holes_y = [self.table_margin, self.resolution[1] - self.table_margin]
            #generates hole locations
            return list(itertools.product(holes_x, holes_y))

        pygame.init()
        pygame.display.set_caption("Gravity Simulator")

        # ball constants
        self.fontObj = pygame.font.Font(pygame.font.get_default_font(), 10)
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

    def create_balls(self,ball_num_txt):
        ball_colors = [
            (0, 200, 200),
            (0, 0, 200),
            (150, 0, 0),
            (200, 0, 200),
            (200, 0, 0),
            (50, 0, 0),
            (100, 0, 0)
        ]

        self.balls = []

        #ball number 0 - players ball
        self.balls.append(
            physics.Ball(self.ball_size, 100, self.resolution[1] / 2, False, (255, 255, 255), 0, ball_num_txt[0])
        )

        for i, color in enumerate(ball_colors):
            self.balls.append(
                physics.Ball(self.ball_size, 100, self.resolution[1] / 2, False, color, i + 1, ball_num_txt[i + 1]))

        self.balls.append(
            physics.Ball(self.ball_size, 100, self.resolution[1] / 2, False, (0, 0, 0), 8, ball_num_txt[i + 1]))


    def set_pool_balls(self, x, y):
        sixty_degrees = math.radians(60)
        # this is used to avoid to the balls touch at all times
        sin_60 = math.sin(sixty_degrees)

        diffx = sin_60 * self.ball_size * 2
        diffy = 0.5 * self.ball_size * 4

        ballx = 0
        bally = 0

        for i, ball in enumerate(self.balls):
            if not i == 0:
                ball.move_to(x + diffx * ballx, y - 0.5 * diffy * (bally * 2 - ballx))
                if bally == ballx:
                    ballx += 1
                    bally = 0
                else:
                    bally += 1


    def main_menu(self):
        #checks if mouse is in a button
        def check_mouse_pos(text_starting_place, text_ending_place, spacing, button_num):
            mouse_pos = pygame.mouse.get_pos()
            return (text_starting_place[button_num][0] - spacing < mouse_pos[0] < text_ending_place[button_num][
                0] + spacing) and \
                    (text_starting_place[button_num][1] - spacing < mouse_pos[1] < text_ending_place[button_num][
                        1] + spacing)

        #draws main menu and returns all the variables needed to check button clicks
        text_starting_place, text_ending_place, spacing, buttons = self.canvas.draw_main_menu(self.table_color)

        was_clicked = False
        button_clicked = 0

        #while a button was not clicked checks if mouse is in the button and if so changes its colour
        while not was_clicked:
            pygame.display.update()
            user_events = graphics.events()

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
        self.canvas.draw_table_sides(self)
        #generates numbers
        ball_num_txt = [(self.fontObj.render(str(num), False, (0, 0, 0)), self.fontObj.size(str(num))) for num in range(16)]

        table_y_middle = self.resolution[1] / 2
        table_x_quarter = 3/4 * self.resolution[0]

        self.create_balls(ball_num_txt)
        self.set_pool_balls(table_x_quarter, table_y_middle)

    def check_for_collision(self):
        collisiontests.check_for_collision(self)

    def do_one_frame(self):
        self.canvas.draw_table_holes(self)
        for ball in self.balls:
            ball.move_once()
        pygame.display.update()
        # self.fps_clock.tick() <----------------------- FIX FPS PLEASE ------------------------------------------

    def all_not_moving(self):
        return_value = True
        for ball in self.balls:
            if not (ball.dx == 0 and ball.dy == 0):
                return_value = False
                break
        return return_value
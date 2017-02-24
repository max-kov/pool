import graphics
import physics
import math
import pygame

class GameState:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Gravity Simulator")

        self.fontObj = pygame.font.Font(pygame.font.get_default_font(), 10)
        self.resolution = [1000, 500]
        self.balls = []
        self.table_margin = 60
        self.ball_size = 13
        self.side_color = (200, 200, 0)
        self.table_color = (0, 100, 0)
        self.cue_color = (100, 100, 100)

        self.canvas = graphics.Canvas(*self.resolution)

    def set_pool_balls(self, x, y, ball_num_txt):
        sixty_degrees = math.radians(60)
        # this is used to avoid to the balls touch at all times
        sin_60 = math.sin(sixty_degrees)

        diffx = sin_60 * self.ball_size * 2
        diffy = 0.5 * self.ball_size * 4

        ballx = 0
        bally = 0

        new_balls = [physics.Planet(self.ball_size, 100, self.resolution[1] / 2, False, (255, 255, 255), 0, ball_num_txt[0])]

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
            new_balls.append(
                physics.Planet(self.ball_size, 100, self.resolution[1] / 2, False, color, i + 1, ball_num_txt[i + 1]))

        new_balls.append(physics.Planet(self.ball_size, 100, self.resolution[1] / 2, False, (0, 0, 0), 8, ball_num_txt[i + 1]))

        for i, color in enumerate(ball_colors):
            new_balls.append(physics.Planet(self.ball_size, 100, self.resolution[1] / 2, True, color, i + 9, ball_num_txt[i + 1]))

        for i, ball in enumerate(new_balls):
            if not i == 0:
                ball.move_to(x + diffx * ballx, y - 0.5 * diffy * (bally * 2 - ballx))
                if bally == ballx:
                    ballx += 1
                    bally = 0
                else:
                    bally += 1

        return new_balls

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
            self.canvas.update()
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

        self.set_pool_balls(table_x_quarter, table_y_middle, ball_num_txt)
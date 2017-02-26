import pygame


# this class gives data about the individual balls
# like the colour or the number on the ball

class BallInfo:
    def __init__(self, ball_number):
        ball_size = 13
        fontObj = pygame.font.Font(pygame.font.get_default_font(), 10)
        ball_num_txt = [(fontObj.render(str(num), False, (0, 0, 0)), fontObj.size(str(num))) for num in range(16)]

        balls_colors = [
            (255, 255, 255),
            (0, 200, 200),
            (0, 0, 200),
            (150, 0, 0),
            (200, 0, 200),
            (200, 0, 0),
            (50, 0, 0),
            (100, 0, 0),
            (0, 0, 0),
            (0, 200, 200),
            (0, 0, 200),
            (150, 0, 0),
            (200, 0, 200),
            (200, 0, 0),
            (50, 0, 0),
            (100, 0, 0)
        ]

        self.ball_color = balls_colors[ball_number]
        self.ball_num_txt = ball_num_txt[ball_number]
        self.ball_size = ball_size
        self.is_striped = ball_number > 8

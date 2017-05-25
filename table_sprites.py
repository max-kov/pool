import numpy as np
import pygame

import config


class Hole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(
            (2 * config.hole_radius, 2 * config.hole_radius))
        # color which will be ignored
        self.image.fill((200, 200, 200))
        self.image.set_colorkey((200, 200, 200))

        pygame.draw.circle(self.image, (0, 0, 0),
                           (config.hole_radius, config.hole_radius), config.hole_radius, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = np.array([x, y])


# this class holds properties of a table side line, but doesn't actually
# draw it
class TableSide():
    def __init__(self, line):
        self.line = np.array(line)
        self.middle = (self.line[0] + self.line[1]) / 2
        self.size = np.round(np.abs(self.line[0] - self.line[1]))
        self.length = np.hypot(*self.size)
        if np.count_nonzero(self.size) != 2:
            # line is perpendicular to y or x axis
            if self.size[0] == 0:
                self.size[0] += 1
            else:
                self.size[1] += 1


# draws the yellow part of the table
class TableColoring(pygame.sprite.Sprite):
    def __init__(self, table_size, color, table_points):
        pygame.sprite.Sprite.__init__(self)
        self.points = table_points
        self.image = pygame.Surface(table_size)
        self.image.fill(color)
        color_key = (200, 200, 200)
        self.image.set_colorkey(color_key)
        pygame.draw.polygon(self.image, color_key, table_points)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def refresh(self):
        self.image.fill(config.table_side_color)
        color_key = (200, 200, 200)
        self.image.set_colorkey(color_key)
        pygame.draw.polygon(self.image, color_key, self.points)

    def update(self, game_state):
        if game_state.stripes_decided:
            font = config.get_default_font(config.ball_radius)
            # generates text at the bottom of the table
            text = [font.render(config.player1_target_text, False, config.player1_cue_color),
                    font.render(config.player2_target_text, False, config.player2_cue_color)]
            start_x = np.array([config.table_margin + config.hole_radius * 3,
                                config.resolution[0] / 2 + config.hole_radius * 3])
            start_y = config.resolution[1] - config.table_margin
            self.image.blit(text[0], [start_x[0], start_y + font.size(config.player1_target_text)[1] / 2])
            self.image.blit(text[1], [start_x[1], start_y + font.size(config.player2_target_text)[1] / 2])
            start_x += font.size(config.player2_target_text)[0]
            for ball in game_state.balls:
                # sorts the balls into their places
                if ball.number != 0 and ball.number != 8:
                    if ball.is_striped:
                        if game_state.player1_stripes:
                            ball.create_image(self.image, (start_x[0], start_y))
                            start_x[0] += config.ball_radius * 2 + config.target_ball_spacing
                        else:
                            ball.create_image(self.image, (start_x[1], start_y))
                            start_x[1] += config.ball_radius * 2 + config.target_ball_spacing
                    else:
                        if not game_state.player1_stripes:
                            ball.create_image(self.image, (start_x[0], start_y))
                            start_x[0] += config.ball_radius * 2 + config.target_ball_spacing
                        else:
                            ball.create_image(self.image, (start_x[1], start_y))
                            start_x[1] += config.ball_radius * 2 + config.target_ball_spacing

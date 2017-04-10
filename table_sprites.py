import pygame
import numpy as np


class Hole(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        self.radius = radius
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2 * radius, 2 * radius))
        # color which will be ignored
        self.image.fill((200, 200, 200))
        self.image.set_colorkey((200, 200, 200))

        pygame.draw.circle(self.image, (0, 0, 0), (radius, radius), radius, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = np.array([x, y])


class TableSide(pygame.sprite.Sprite):
    def __init__(self, color, rect, is_vertical, trigger_on_min):
        pygame.sprite.Sprite.__init__(self)

        self.is_vertical = is_vertical
        self.trigger_on_min = trigger_on_min

        self.x_min = min(rect[0], rect[2])
        self.y_min = min(rect[1], rect[3])
        self.x_max = max(rect[0], rect[2])
        self.y_max = max(rect[1], rect[3])

        self.width = rect[2] - rect[0]
        self.height = rect[3] - rect[1]

        self.image = pygame.Surface((self.width, self.height))
        # color which will be ignored
        self.image.fill((200, 200, 200))
        self.image.set_colorkey((200, 200, 200))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = [rect[0] + self.width / 2.0, rect[1] + self.height / 2.0]

    def ball_hit(self, ball):
        if self.is_vertical:
            if ball.pos[0] + ball.radius >= self.x_min and ball.velocity[0] > 0 and self.trigger_on_min:
                ball.velocity[0] *= -1
            elif ball.pos[0] - ball.radius <= self.x_max and ball.velocity[0] < 0 and not self.trigger_on_min:
                ball.velocity[0] *= -1

        if not self.is_vertical:
            if ball.pos[1] + ball.radius > self.y_min and ball.velocity[1] > 0 and self.trigger_on_min:
                ball.velocity[1] *= -1
            elif ball.pos[1] - ball.radius < self.y_max and ball.velocity[1] < 0 and not self.trigger_on_min:
                ball.velocity[1] *= -1


class TriangleSide(pygame.sprite.Sprite):
    def __init__(self, color, triangle):
        pygame.sprite.Sprite.__init__(self)

        self.line = np.array(triangle)
        self.size = np.abs(self.line[0] - self.line[1] + 1)
        self.image = pygame.Surface(self.size)

        self.image.fill((200, 200, 200))
        self.image.set_colorkey((200, 200, 200))
        if np.all(np.less_equal(self.line[0] - self.line[1], 0)) or np.all(
                np.greater_equal(self.line[0] - self.line[1], 0)):
            pygame.draw.line(self.image, color, [0, 0], self.size - 1)
        else:
            pygame.draw.line(self.image, color, [0, self.size[1]], [self.size[0], 0])
        self.rect = self.image.get_rect()
        self.rect.center = (self.line[0] + self.line[1]) / 2

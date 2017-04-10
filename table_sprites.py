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

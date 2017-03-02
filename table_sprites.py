import pygame


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
        self.x = x
        self.y = y

class TableSide(pygame.sprite.Sprite):
    def __init__(self, rect, color):
        pygame.sprite.Sprite.__init__(self)

        self.width = rect[2] - rect[0]
        self.height = rect[3] - rect[1]

        self.image = pygame.Surface((self.width, self.height))
        # color which will be ignored
        self.image.fill((200, 200, 200))
        self.image.set_colorkey((200, 200, 200))

        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = [rect[0] + self.width / 2.0, rect[1] + self.height / 2.0]

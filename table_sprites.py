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
    def __init__(self, color, rect, change_on_hit):
        pygame.sprite.Sprite.__init__(self)

        self.x_min = min(rect[0],rect[2])
        self.y_min = min(rect[1],rect[3])
        self.x_max = max(rect[0],rect[2])
        self.y_max = max(rect[1],rect[3])

        self.width = rect[2] - rect[0]
        self.height = rect[3] - rect[1]

        self.image = pygame.Surface((self.width, self.height))
        # color which will be ignored
        self.image.fill((200, 200, 200))
        self.image.set_colorkey((200, 200, 200))

        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = [rect[0] + self.width / 2.0, rect[1] + self.height / 2.0]

        # this multiplies the balls dy, dx by values stored in on hit
        self.on_hit = change_on_hit

    def ball_hit(self,ball):
        if self.on_hit[0]<0:
            if ball.x + ball.radius > self.x_min and ball.dx > 0:
                ball.dx *= self.on_hit[0]
            elif ball.x - ball.radius < self.x_max and ball.dx < 0:
                ball.dx *= self.on_hit[0]

        if self.on_hit[1]<0:
            if ball.y + ball.radius > self.y_min and ball.dy > 0:
                ball.dy *= self.on_hit[1]
            elif ball.y - ball.radius < self.y_max and ball.dy < 0:
                ball.dy *= self.on_hit[1]


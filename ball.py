import pygame
import math
import numpy as np


class Ball(pygame.sprite.Sprite):
    def __init__(self, ball_number):
        # constants
        ball_size = 13
        fontObj = pygame.font.Font(pygame.font.get_default_font(), 10)

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

        self.text = fontObj.render(str(ball_number), False, (0, 0, 0))
        self.text_length = np.array(fontObj.size(str(ball_number)))
        self.color = balls_colors[ball_number]
        self.radius = ball_size
        self.mass = ball_size
        self.is_striped = ball_number > 8
        self.number = ball_number

        self.pos = np.zeros(2)
        self.velocity = np.zeros(2)
        self.sprite_offset = np.zeros(2)

        pygame.sprite.Sprite.__init__(self)
        self.update_sprite()

    def move_to(self, pos):
        self.pos = pos
        self.rect.center = self.pos

    def add_force(self, force):
        self.velocity += force/self.mass

    def update(self, game_state, scale=1):
        self.pos += self.velocity
        self.velocity *= game_state.friction_coeff

        if abs(self.velocity[1]) < 0.01:
            self.velocity[1] = 0

        if abs(self.velocity[0]) < 0.01:
            self.velocity[0] = 0

        self.top_left = self.pos - self.radius
        self.rect.center = self.pos.tolist()

    def set_vector(self, delta_v):
        self.velocity = delta_v

    def update_sprite(self):
        new_sprite = pygame.Surface([self.radius * 2, self.radius * 2])
        new_sprite.fill((200, 200, 200))
        new_sprite.set_colorkey((200, 200, 200))

        pygame.draw.circle(new_sprite, self.color, (self.radius, self.radius), self.radius)

        if self.is_striped and self.number != 0:
            arc_angle = math.radians(20)
            step = arc_angle / 10

            right_side_points =np.column_stack((np.cos(np.arange(-arc_angle, arc_angle, step)),
                                          np.sin(np.arange(-arc_angle, arc_angle, step))))
            left_side_points = np.column_stack((np.cos(np.arange(-arc_angle + np.pi, arc_angle + np.pi, step)),
                                  np.sin(np.arange(-arc_angle + np.pi, arc_angle + np.pi, step))))

            point_list = np.concatenate((left_side_points,right_side_points))
            point_list *= self.radius * 0.8
            point_list += self.radius

            pygame.draw.polygon(new_sprite, (255, 255, 255), list(map(tuple,point_list)))

        pygame.draw.circle(new_sprite, (255, 255, 255), (self.radius, self.radius), self.radius / 2)
        if self.number!=0:
            new_sprite.blit(self.text, tuple(self.radius - self.text_length / 2))

        self.image = new_sprite
        self.rect = self.image.get_rect()
        self.top_left = self.pos - self.radius

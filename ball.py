import pygame
import math
import numpy as np


class Ball(pygame.sprite.Sprite):
    def __init__(self, ball_data):
        pygame.sprite.Sprite.__init__(self)

        self.mass = ball_data.ball_size
        self.pos = np.array([0, 0], dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.radius = ball_data.ball_size
        self.is_striped = ball_data.is_striped
        self.color = ball_data.ball_color
        self.number = ball_data.ball_number
        self.number_text = ball_data.number_text
        self.text_length = ball_data.number_text_size
        self.sprite_offset = [0, 0]

        self.update_sprite()

    def move_to(self, pos_x, pos_y):
        self.pos = np.array([pos_x, pos_y], dtype=float)
        self.rect.center = self.pos

    def add_force(self, delta_x, delta_y):
        self.velocity += [delta_x / self.mass, delta_y / self.mass]

    def update(self, game_state, scale=1):
        self.pos += self.velocity
        self.velocity *= game_state.friction_coeff

        if abs(self.velocity[1]) < 0.01:
            self.velocity[1] = 0

        if abs(self.velocity[0]) < 0.01:
            self.velocity[0] = 0

        self.top_left = self.pos - self.radius
        self.rect.center = self.pos.tolist()

    def set_vector(self, delta_x, delta_y):
        self.velocity = np.array([delta_x, delta_y], dtype=float)

    def update_sprite(self):
        new_sprite = pygame.Surface([self.radius * 2, self.radius * 2])
        new_sprite.fill((200, 200, 200))
        new_sprite.set_colorkey((200, 200, 200))

        pygame.draw.circle(new_sprite, self.color, (self.radius, self.radius), self.radius)

        if self.is_striped and not self.number == 0:
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
        new_sprite.blit(self.number_text,tuple(self.radius-self.text_length/2))

        self.image = new_sprite
        self.rect = self.image.get_rect()
        self.top_left = self.pos - self.radius

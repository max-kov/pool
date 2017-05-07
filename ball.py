import math
import numpy as np
import pygame

from physics import rotation_matrix
from config import *


class Ball(pygame.sprite.Sprite):
    def __init__(self, ball_number, pygame_initialised=True):
        self.color = ball_colors[ball_number]
        self.is_striped = ball_number > 8

        if self.is_striped:
            # every point is a 3d coordinate on the ball
            # a circle will be drawn on the point if its Z component is >0 (is
            # visible)
            point_num = 50
            self.stripe_circle = ball_radius * np.column_stack((np.cos(np.linspace(0, 2 * np.pi, point_num)),
                                                                np.sin(np.linspace(0, 2 * np.pi, point_num)), np.zeros(point_num)))
        else:
            self.stripe_circle = []

        self.number = ball_number
        self.pos = np.zeros(2, dtype = float)
        self.velocity = np.zeros(2, dtype = float)
        # initial location of the white circle and number on the ball, a.k.a
        # ball label
        self.label_offset = np.array([0, 0, ball_radius])
        self.label_size = ball_radius // 2

        # if pygame was not initialised (like when testing)
        # the class wont try to create fonts and update
        if pygame_initialised:
            pygame.sprite.Sprite.__init__(self)
            font_obj = get_default_font(ball_label_text_size)
            self.text = font_obj.render(str(ball_number), False, (0, 0, 0))
            self.text_length = np.array(font_obj.size(str(ball_number)))
            self.update()

    def move_to(self, pos):
        self.pos = np.array(pos, dtype = float)

    def add_force(self, force, time=1):
        # f = ma, v = u + at -> v = u + (f/m)*t
        self.velocity += (force / ball_mass) * time

    def update(self):
        self.velocity *= friction_coeff
        self.pos += self.velocity

        if np.count_nonzero(self.velocity) > 0:
            # updates label circle and number offset
            perpendicular_velocity = -np.cross(self.velocity,[0,0,1])
            # angle formula is angle=((ballspeed*2)/(pi*r*2))*2
            rotation_angle = np.hypot(
                *(self.velocity)) * 2 / (ball_radius * np.pi)
            transformation_matrix = rotation_matrix(
                perpendicular_velocity, -rotation_angle)
            self.label_offset = np.matmul(
                self.label_offset, transformation_matrix)
            for i, stripe in enumerate(self.stripe_circle):
                self.stripe_circle[i] = np.matmul(
                    stripe, transformation_matrix)

        if np.hypot(*self.velocity) < friction_threshold:
            self.velocity = np.zeros(2)

        self.update_sprite()
        self.top_left = self.pos - ball_radius
        self.rect.center = self.pos.tolist()

    def set_vector(self, new_velocity):
        self.velocity = np.array(new_velocity, dtype = float)

    def update_sprite(self):
        sprite_dimension = np.repeat([ball_radius * 2], 2)
        new_sprite = pygame.Surface(sprite_dimension)
        colorkey = (200, 200, 200)
        new_sprite.fill(self.color)
        new_sprite.set_colorkey(colorkey)

        label_dimension = np.repeat([self.label_size * 2], 2)
        label = pygame.Surface(label_dimension)
        label.fill(self.color)
        # 1.1 instead of 1 is a hack to avoid 0 width sprite when scaling
        dist_from_centre = 1.1 - (self.label_offset[0] ** 2 +
                                  self.label_offset[1] ** 2) / (ball_radius ** 2)

        if self.label_offset[2] > 0:
            pygame.draw.circle(label, (255, 255, 255),
                               label_dimension // 2, self.label_size)

            if self.number != 0:
                label.blit(self.text, (ball_radius - self.text_length) / 2)

            # hack to avoid div by zero
            if self.label_offset[0] != 0:
                angle = -math.degrees(
                    math.atan(self.label_offset[1] / self.label_offset[0]))
                label = pygame.transform.scale(
                    label, (int(ball_radius * dist_from_centre), ball_radius))
                label = pygame.transform.rotate(label, angle)

        new_sprite.blit(
            label, self.label_offset[:2] + (sprite_dimension - label.get_size()) / 2)
        for num, point in enumerate(self.stripe_circle):
            if point[2] >= -1:
                # ball.stripe_thickness*(1 + point[2]/ball.radius)) makes the circles
                # near the edges smaller and circles on the top bigger
                pygame.draw.circle(new_sprite, (255, 255, 255), ball_radius + point[:2].astype(int),
                                   int(ball_stripe_thickness * (1 + point[2] / ball_radius)))

        # applies a circular mask on the sprite using colorkey
        grid_2d = np.mgrid[-ball_radius:ball_radius +
                           1, -ball_radius:ball_radius + 1]
        is_outside = ball_radius < np.hypot(*grid_2d)

        for counter_x in range(ball_radius * 2 + 1):
            for counter_y in range(ball_radius * 2 + 1):
                if is_outside[counter_x, counter_y]:
                    new_sprite.set_at([counter_x, counter_y], colorkey)

        self.image = new_sprite
        self.rect = self.image.get_rect()
        self.top_left = self.pos - ball_radius

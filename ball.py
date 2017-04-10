import math
import numpy as np
import pygame

from physics import rotation_matrix


class Ball(pygame.sprite.Sprite):
    def __init__(self, ball_number, ball_size, friction_coeff):
        font_obj = pygame.font.Font(pygame.font.get_default_font(), 10)

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

        self.text = font_obj.render(str(ball_number), False, (0, 0, 0))
        self.text_length = np.array(font_obj.size(str(ball_number)))
        self.color = balls_colors[ball_number]
        self.radius = ball_size
        self.mass = ball_size
        self.is_striped = ball_number > 8
        self.friction_coeff = friction_coeff

        if self.is_striped:
            # every point is a 3d coordinate on the ball
            # a circle will be drawn on the point if its Z component is >0 (is visible)
            point_num = 50
            self.stripe_circle = self.radius * np.column_stack((np.cos(np.linspace(0, 2 * np.pi, point_num)),
                                                                np.sin(np.linspace(0, 2 * np.pi, point_num)),
                                                                np.zeros(point_num)))
        else:
            self.stripe_circle = []

        self.stripe_thickness = 2
        self.number = ball_number
        self.pos = np.zeros(2)
        self.velocity = np.zeros(2)
        # initial location of the white circle and number on the ball, a.k.a label
        self.label_offset = np.array([0, 0, self.radius])
        self.label_size = self.radius / 2

        pygame.sprite.Sprite.__init__(self)
        self.update_sprite()

    def move_to(self, pos):
        self.pos = pos
        self.rect.center = self.pos

    def add_force(self, force, time=1):
        # f = ma, v = u + at -> v = u + (f/m)*t
        self.velocity += (force / self.mass) * time

    def update(self):
        self.velocity *= self.friction_coeff
        self.pos += self.velocity

        if np.count_nonzero(self.velocity) > 0:
            # updates small circle and number offset
            perpendicular_velocity = np.array([-self.velocity[1], self.velocity[0], 0])
            # angle formula is angle=((ballspeed*2)/(pi*r*2))*2
            rotation_angle = np.hypot(*(self.velocity)) * 2 / (self.radius * np.pi)
            transformation_matrix = rotation_matrix(perpendicular_velocity, -rotation_angle)
            self.label_offset = np.matmul(self.label_offset, transformation_matrix)
            for i, stripe in enumerate(self.stripe_circle):
                self.stripe_circle[i] = np.matmul(stripe, transformation_matrix)

        for i,vel_component in enumerate(self.velocity):
            if abs(vel_component) < 0.06:
                self.velocity[i] = 0

        self.update_sprite()
        self.top_left = self.pos - self.radius
        self.rect.center = self.pos.tolist()

    def set_vector(self, new_velocity):
        self.velocity = new_velocity

    def update_sprite(self):
        sprite_dimension = np.repeat([self.radius * 2 + 1], 2)
        new_sprite = pygame.Surface(sprite_dimension)
        colorkey = (200, 200, 200)
        new_sprite.fill(self.color)
        new_sprite.set_colorkey(colorkey)

        label_dimension = np.repeat([self.label_size * 2 + 1], 2)
        label = pygame.Surface(label_dimension)
        label.fill(self.color)
        # 1.1 instead of 1 is a hack to avoid 0 width sprite when scaling
        dist_from_centre = 1.1 - ((self.label_offset[0] ** 2 + self.label_offset[1] ** 2) / (self.radius ** 2))

        if self.label_offset[2] > 0:
            pygame.draw.circle(label, (255, 255, 255), label_dimension / 2, self.label_size)

            if self.number != 0:
                label.blit(self.text, (self.radius - self.text_length) / 2)

            # hack to avoid div by zero
            if self.label_offset[0] != 0:
                angle = - math.degrees(math.atan(self.label_offset[1] / self.label_offset[0]))
                label = pygame.transform.scale(label, (int(self.radius * dist_from_centre), self.radius))
                label = pygame.transform.rotate(label, angle)

        new_sprite.blit(label, self.label_offset[:2] + (sprite_dimension - label.get_size()) / 2)
        for num, point in enumerate(self.stripe_circle):
            if point[2] >= -1:
                # ball.stripe_thickness*(1 + point[2]/ball.radius)) makes the circles
                # near the edges smaller and circles on the top bigger
                pygame.draw.circle(new_sprite, (255, 255, 255), self.radius + point[:2].astype(int),
                                   int(self.stripe_thickness * (1 + point[2] / self.radius)))

        # applies a circular mask on the sprite using colorkey
        grid_2d = np.mgrid[-self.radius:self.radius + 1, -self.radius:self.radius + 1]
        is_outside = self.radius < np.hypot(*grid_2d)

        for counter_x in range(self.radius * 2 + 1):
            for counter_y in range(self.radius * 2 + 1):
                if is_outside[counter_x, counter_y]:
                    new_sprite.set_at([counter_x, counter_y], colorkey)

        self.image = new_sprite
        self.rect = self.image.get_rect()
        self.top_left = self.pos - self.radius

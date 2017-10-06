import itertools
import math
from enum import Enum

import numpy as np
import pygame

import collisions
import config
import event
import physics


class Ball():
    def __init__(self):
        self.pos = np.zeros(2, dtype=float)
        self.velocity = np.zeros(2, dtype=float)

    def apply_force(self, force, time=1):
        # f = ma, v = u + at -> v = u + (f/m)*t
        self.velocity += (force / config.ball_mass) * time

    def set_velocity(self, new_velocity):
        self.velocity = np.array(new_velocity, dtype=float)

    def move_to(self, pos):
        self.pos = np.array(pos, dtype=float)

    def update(self, *args):
        self.velocity *= config.friction_coeff
        self.pos += self.velocity

        if np.hypot(*self.velocity) < config.friction_threshold:
            self.velocity = np.zeros(2)


class BallType(Enum):
    Striped = "striped"
    Solid = "solid"


class StripedBall():
    def __init__(self):
        # every point is a 3d coordinate on the ball
        # a circle will be drawn on the point if its Z component is >0 (is
        # visible)
        point_num = config.ball_stripe_point_num
        self.stripe_circle = config.ball_radius * np.column_stack((np.cos(np.linspace(0, 2 * np.pi, point_num)),
                                                                   np.sin(np.linspace(
                                                                       0, 2 * np.pi, point_num)),
                                                                   np.zeros(point_num)))

    def update_stripe(self, transformation_matrix):
        for i, stripe in enumerate(self.stripe_circle):
            self.stripe_circle[i] = np.matmul(
                stripe, transformation_matrix)

    def draw_stripe(self, sprite):
        for num, point in enumerate(self.stripe_circle[:-1]):
            if point[2] >= -1:
                pygame.draw.line(sprite, (255, 255, 255), config.ball_radius + point[:2],
                                 config.ball_radius + self.stripe_circle[num + 1][:2], config.ball_stripe_thickness)


class SolidBall():
    def __init__(self):
        pass


class BallSprite(pygame.sprite.Sprite):
    def __init__(self, ball_number):
        self.number = ball_number
        self.color = config.ball_colors[ball_number]
        if ball_number <= 8:
            self.ball_type = BallType.Solid
            self.ball_stripe = SolidBall()
        else:
            self.ball_type = BallType.Striped
            self.ball_stripe = StripedBall()
        self.ball = Ball()
        pygame.sprite.Sprite.__init__(self)
        # initial location of the white circle and number on the ball, a.k.a
        # ball label
        self.label_offset = np.array([0, 0, config.ball_radius])
        self.label_size = config.ball_radius // 2
        font_obj = config.get_default_font(config.ball_label_text_size)
        self.text = font_obj.render(str(ball_number), False, (0, 0, 0))
        self.text_length = np.array(font_obj.size(str(ball_number)))
        self.update_sprite()
        self.update()
        self.top_left = self.ball.pos - config.ball_radius
        self.rect.center = self.ball.pos.tolist()

    def update(self, *args):
        if np.hypot(*self.ball.velocity) != 0:
            # updates label circle and number offset
            perpendicular_velocity = -np.cross(self.ball.velocity, [0, 0, 1])
            # angle formula is angle=((ballspeed*2)/(pi*r*2))*2
            rotation_angle = -np.hypot(
                *(self.ball.velocity)) * 2 / (config.ball_radius * np.pi)
            transformation_matrix = physics.rotation_matrix(
                perpendicular_velocity, rotation_angle)
            self.label_offset = np.matmul(
                self.label_offset, transformation_matrix)
            if self.ball_type == BallType.Striped:
                self.ball_stripe.update_stripe(transformation_matrix)
            self.update_sprite()
            self.ball.update()

    def update_sprite(self):
        sprite_dimension = np.repeat([config.ball_radius * 2], 2)
        new_sprite = pygame.Surface(sprite_dimension)
        colorkey = (200, 200, 200)
        new_sprite.fill(self.color)
        new_sprite.set_colorkey(colorkey)

        label_dimension = np.repeat([self.label_size * 2], 2)
        label = pygame.Surface(label_dimension)
        label.fill(self.color)
        # 1.1 instead of 1 is a hack to avoid 0 width sprite when scaling
        dist_from_centre = 1.1 - (self.label_offset[0] ** 2 +
                                  self.label_offset[1] ** 2) / (config.ball_radius ** 2)

        if self.label_offset[2] > 0:
            pygame.draw.circle(label, (255, 255, 255),
                               label_dimension // 2, self.label_size)

            if self.number != 0:
                label.blit(self.text, (config.ball_radius - self.text_length) / 2)

            # hack to avoid div by zero
            if self.label_offset[0] != 0:
                angle = -math.degrees(
                    math.atan(self.label_offset[1] / self.label_offset[0]))
                label = pygame.transform.scale(
                    label, (int(config.ball_radius * dist_from_centre), config.ball_radius))
                label = pygame.transform.rotate(label, angle)

        new_sprite.blit(
            label, self.label_offset[:2] + (sprite_dimension - label.get_size()) / 2)
        if self.ball_type == BallType.Striped:
            self.ball_stripe.draw_stripe(new_sprite)

        # applies a circular mask on the sprite using colorkey
        grid_2d = np.mgrid[-config.ball_radius:config.ball_radius +
                                               1, -config.ball_radius:config.ball_radius + 1]
        is_outside = config.ball_radius < np.hypot(*grid_2d)

        for xy in itertools.product(range(config.ball_radius * 2 + 1), repeat=2):
            if is_outside[xy]:
                new_sprite.set_at(xy, colorkey)

        self.image = new_sprite
        self.rect = self.image.get_rect()
        self.top_left = self.ball.pos - config.ball_radius
        self.rect.center = self.ball.pos.tolist()

    def create_image(self, surface, coords):
        surface.blit(self.image, coords)

    def is_clicked(self, events):
        return physics.distance_less_equal(events["mouse_pos"], self.ball.pos, config.ball_radius)

    def move_to(self, pos):
        self.ball.move_to(pos)
        self.rect.center = self.ball.pos.tolist()

    def is_active(self, game_state, behind_separation_line=False):
        game_state.cue.make_invisible()
        events = event.events()

        while events["clicked"]:
            events = event.events()
            # checks if the user isn't trying to place the ball out of the table or inside another ball
            if np.all(np.less(config.table_margin + config.ball_radius + config.hole_radius, events["mouse_pos"])) and \
                    np.all(np.greater(config.resolution - config.table_margin - config.ball_radius - config.hole_radius,
                                      events["mouse_pos"])) and \
                    not collisions.check_if_ball_touches_balls(events["mouse_pos"], self.number, game_state.balls):
                if behind_separation_line:
                    if events["mouse_pos"][0] <= config.white_ball_initial_pos[0]:
                        self.move_to(events["mouse_pos"])
                else:
                    self.move_to(events["mouse_pos"])
            game_state.redraw_all()
        game_state.cue.make_visible(game_state.current_player)

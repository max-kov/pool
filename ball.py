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
        self.sprite_visible = True
        self.sprite_size = self.radius/2

        pygame.sprite.Sprite.__init__(self)
        self.update_sprite()

    def move_to(self, pos):
        self.pos = pos
        self.rect.center = self.pos

    def add_force(self, force):
        self.velocity += force/self.mass

    def update(self, game_state, scale=1):
        self.pos += self.velocity
        if self.sprite_visible:
            self.sprite_offset += self.velocity
        else:
            self.sprite_offset -= self.velocity
        if np.hypot(*self.sprite_offset)>self.radius+self.sprite_size:
            self.sprite_visible = not self.sprite_visible
        self.velocity *= game_state.friction_coeff

        if abs(self.velocity[1]) < 0.01:
            self.velocity[1] = 0

        if abs(self.velocity[0]) < 0.01:
            self.velocity[0] = 0

        self.update_sprite()
        self.top_left = self.pos - self.radius
        self.rect.center = self.pos.tolist()

    def set_vector(self, delta_v):
        self.velocity = delta_v

    def update_sprite(self):
        sprite_size = np.repeat([self.radius*2],2)

        new_sprite = pygame.Surface(sprite_size)
        new_sprite.fill((200, 200, 200))
        new_sprite.set_colorkey((200, 200, 200))

        pygame.draw.circle(new_sprite, self.color, sprite_size/2, self.radius)

        if self.sprite_visible:
            pygame.draw.circle(new_sprite, (255, 255, 255), self.sprite_offset.astype(int)+[self.radius, self.radius], self.sprite_size)
            if self.number!=0:
                new_sprite.blit(self.text, (self.radius - self.text_length / 2)+self.sprite_offset.astype(int))
                # used to remove part of the sprite which is outside the ball
                triag1 = np.array(([0, 0], [self.radius / 2, 0], [0, self.radius / 2]))
                triag2 = np.array(([0, 2*self.radius], [self.radius / 2, 2*self.radius], [0, 3*self.radius / 2]))
                triag3 = np.array(([2*self.radius, 0], [2*self.radius, self.radius / 2], [3*self.radius / 2,0]))
                triag4 = np.array(([2*self.radius, 2*self.radius], [3*self.radius / 2, 2*self.radius], [2*self.radius, 3*self.radius / 2]))
                pygame.draw.polygon(new_sprite,(200,200,200),triag1)
                pygame.draw.polygon(new_sprite, (200, 200, 200), triag2)
                pygame.draw.polygon(new_sprite, (200, 200, 200), triag3)
                pygame.draw.polygon(new_sprite, (200, 200, 200), triag4)


        pygame.draw.circle(new_sprite, (200,200,200), sprite_size/2, self.radius+6,6)
        self.image = new_sprite
        self.rect = self.image.get_rect()
        self.top_left = self.pos - self.radius

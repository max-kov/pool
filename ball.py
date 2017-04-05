import pygame
from physics import rotation_matrix
import numpy as np
import math


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
        self.sprite_offset = np.array([0,0,self.radius])
        self.sprite_visible = True
        self.sprite_size = self.radius/2

        pygame.sprite.Sprite.__init__(self)
        self.update_sprite()

    def move_to(self, pos):
        self.pos = pos
        self.rect.center = self.pos

    def add_force(self, force):
        self.velocity += force/self.mass

    def update(self, game_state):
        self.pos += self.velocity
        self.velocity *= game_state.friction_coeff


        if np.count_nonzero(self.velocity)>0:
            # updates small circle and number offset
            perpendicular_velocity = np.array([-self.velocity[1],self.velocity[0],0])
            rotation_angle = np.hypot(*(self.velocity*2))/(self.radius*np.pi*2)
            self.sprite_offset = np.matmul(self.sprite_offset,rotation_matrix(perpendicular_velocity,-rotation_angle))

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
        def remove_excess(sprite,colorkey,radius):
            x = np.arange(-radius,radius+1)
            y = np.arange(-radius,radius+1)
            x, y = np.meshgrid(x, y)
            is_outside = radius**2 < (x**2 + y**2)

            out_sprite = sprite

            for counter_x in range(radius*2+1):
                for counter_y in range(radius*2+1):
                    if is_outside[counter_x,counter_y]:
                        out_sprite.set_at([counter_x,counter_y],colorkey)
            return out_sprite
        sprite_size = np.repeat([self.radius*2],2)

        new_sprite = pygame.Surface(sprite_size)
        colorkey = (200, 200, 200)
        new_sprite.fill(colorkey)
        new_sprite.set_colorkey(colorkey)

        pygame.draw.circle(new_sprite, self.color, sprite_size/2, self.radius)

        if self.sprite_offset[2]>0:
            sprite_shift = self.sprite_offset[:2].astype(int)
            pygame.draw.circle(new_sprite, (255, 255, 255), sprite_shift+self.radius, self.sprite_size)
            if self.number!=0:
                new_sprite.blit(self.text,(self.radius - self.text_length / 2)+sprite_shift)

        self.image = remove_excess(new_sprite,colorkey,self.radius)
        self.rect = self.image.get_rect()
        self.top_left = self.pos - self.radius

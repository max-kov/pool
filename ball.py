import pygame
from physics import rotation_matrix
import numpy as np
import math


class Ball(pygame.sprite.Sprite):
    def __init__(self, ball_number, ball_size):
        # constants
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
        if self.is_striped:
            self.stripe_circle = self.radius*np.column_stack((np.cos(np.linspace(0,2*np.pi,50)),
                                                              np.sin(np.linspace(0,2*np.pi,50)),
                                                              np.zeros(50)))
        else:
            self.stripe_circle = []

        self.stripe_thickness = 5
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

        if np.count_nonzero(self.velocity)>0:
            # updates small circle and number offset
            perpendicular_velocity = np.array([-self.velocity[1],self.velocity[0],0])
            rotation_angle = np.hypot(*(self.velocity))*2/(self.radius*np.pi)
            transformation_matrix = rotation_matrix(perpendicular_velocity,-rotation_angle)
            self.sprite_offset = np.matmul(self.sprite_offset,transformation_matrix)
            for i,stripe in enumerate(self.stripe_circle):
                self.stripe_circle[i] = np.matmul(stripe,transformation_matrix)

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

        def render_small_circle(ball,offset,size):
            small_circle = pygame.Surface(size)
            small_circle.fill(ball.color)
            # 1.1 instead of 1 is a hack to avoid 0 width sprite when rounding
            dist_from_centre = 1.1 - ((offset[0] ** 2 + offset[1] ** 2) / (ball.radius ** 2))

            if offset[2] > 0:
                pygame.draw.circle(small_circle, (255, 255, 255), size/2, ball.sprite_size)

                if ball.number != 0:
                    small_circle.blit(ball.text, (size - ball.text_length)/2)

                # hack to avoid div by zero
                if not offset[0]==0:
                    angle = - math.degrees(math.atan(offset[1] / offset[0]))
                    small_circle = pygame.transform.scale(small_circle, (int(size[0] * dist_from_centre), size[1]))
                    small_circle = pygame.transform.rotate(small_circle, angle)

            return small_circle

        def draw_stripe(ball,sprite):
            for num,point in enumerate(self.stripe_circle):
                if point[2]>=-1:
                    pygame.draw.line(sprite, (255, 255, 255), ball.radius + self.stripe_circle[num-1][:2],
                                 ball.radius+point[:2], int(ball.stripe_thickness*(1 + point[2]/ball.radius)))

        sprite_size = np.repeat([self.radius*2+1],2)

        new_sprite = pygame.Surface(sprite_size)
        colorkey = (200, 200, 200)
        new_sprite.fill(self.color)
        new_sprite.set_colorkey(colorkey)

        small_sprite = render_small_circle(self,self.sprite_offset,sprite_size)
        new_sprite.blit(small_sprite,self.sprite_offset[:2]+(sprite_size - small_sprite.get_size())/2)
        draw_stripe(self,new_sprite)

        self.image = remove_excess(new_sprite,colorkey,self.radius)
        self.rect = self.image.get_rect()
        self.top_left = self.pos - self.radius

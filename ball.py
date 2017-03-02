import pygame
import math

friction_coeff = 0.994


class Ball(pygame.sprite.Sprite):
    def __init__(self, ball_mass, planet_x, planet_y,is_striped,color,number,number_text):
        pygame.sprite.Sprite.__init__(self)

        self.mass = ball_mass
        self.x = planet_x
        self.y = planet_y
        self.dx = 0
        self.dy = 0
        self.radius = ball_mass
        self.is_striped = is_striped
        self.color = color
        self.number = number
        self.number_info = number_text

        self.update_sprite()

    def move_to(self, game_state, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

        self.rect.center = (self.x, self.y)

    def add_force(self, delta_x, delta_y):
        self.dx += delta_x / self.mass
        self.dy += delta_y / self.mass

    def update(self, game_state, scale=1):
        tempx = self.x + self.dx*scale
        tempy = self.y + self.dy*scale
        self.move_to(game_state, tempx, tempy)
        self.dx = self.dx*friction_coeff
        self.dy = self.dy*friction_coeff

        if abs(self.dy)<0.01:
            self.dy = 0

        if abs(self.dx) < 0.01:
            self.dx = 0

        self.top_left = (self.x - self.radius, self.y - self.radius)

        self.rect.center = (self.x,self.y)

    def set_vector(self, delta_x, delta_y):
        self.dx = delta_x
        self.dy = delta_y

    # def destroy(self, game_state):
    #     game_state.canvas.delete_ball(game_state, self)

    def update_sprite(self):
        new_sprite = pygame.Surface([self.radius * 2, self.radius * 2])
        new_sprite.fill((200,200,200))
        new_sprite.set_colorkey((200,200,200))

        pygame.draw.circle(new_sprite, self.color, (self.radius, self.radius), self.radius)

        if self.is_striped and not self.number==0:
            point_list = [(self.radius + math.cos(math.radians(angle)) * self.radius * 0.8,
                           self.radius + math.sin(math.radians(angle)) * self.radius * 0.8) for angle
                          in range(20,-20,-1)]
            point_list+=[(self.radius + math.cos(math.radians(angle)) * self.radius * 0.8,
                          self.radius + math.sin(math.radians(angle)) * self.radius * 0.8) for angle
                         in range(200,160,-1)]
            pygame.draw.polygon(new_sprite, (255, 255, 255), point_list)

        pygame.draw.circle(new_sprite, (255, 255, 255), (self.radius, self.radius), self.radius / 2)
        new_sprite.blit(self.number_info[0], (self.radius - self.number_info[1][0] / 2, self.radius - self.number_info[1][1] / 2))

        self.image = new_sprite
        self.rect = self.image.get_rect()
        self.top_left = (self.x - self.radius, self.y - self.radius)
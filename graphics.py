import pygame

class Game_Window():
    def __init__(self, vertical_size, horizontal_size, *args, **kwargs):
        pygame.init()
        self.surface = pygame.display.set_mode((vertical_size, horizontal_size), *args, **kwargs)
        self.size_x = vertical_size
        self.size_y = horizontal_size

        #fps control
        self.fps_clock = pygame.time.Clock()
        self.fps_limit = 60

    def update(self):
        pygame.display.update()

    def move_all_once(self,planets):
        for planet in planets:
            planet.move_once(self)
        self.update()
        self.fps_clock.tick(self.fps_limit)




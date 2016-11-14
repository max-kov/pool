import pygame




class Game_Window():
    def __init__(self,vertical_size,horizontal_size,*args,**kwargs):
        self.surface = pygame.display.set_mode((vertical_size,horizontal_size),*args,**kwargs)
        self.size_x = vertical_size
        self.size_y = horizontal_size

    def update(self):
        pygame.display.update()

class Planet():
    def __init__(self, game_window, planet_mass, planet_x, planet_y, *args):
        self.mass = planet_mass
        self.x = planet_x
        self.y = planet_y

        pygame.draw.circle(game_window.surface,(255,255,255),(planet_x,planet_y),3)

    def move_to(self,game_window,pos_x,pos_y):
        pygame.draw.circle(game_window.surface, (0,0,0), (self.x, self.y), 3)
        pygame.draw.circle(game_window.surface, (255, 255, 255), (pos_x, pos_y), 3)

        self.x = pos_x
        self.y = pos_y

#opened for testing
if __name__=='__main__':
    pygame.init()
    window = Game_Window(500,500)
    mars = Planet(window,100,50,50)
    window.update()
    fps_clock = pygame.time.Clock()
    fps_limit = 60

    for coord in range(50,400):
        mars.move_to(window,coord,coord)
        window.update()

        fps_clock.tick(fps_limit)

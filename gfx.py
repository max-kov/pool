import pygame,physics

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
        self.dx = 0
        self.dy = 0

        pygame.draw.circle(game_window.surface,(255,255,255),(planet_x,planet_y),3)

    def move_to(self,game_window,pos_x,pos_y):
        pygame.draw.circle(game_window.surface, (0,0,0), (int(self.x), int(self.y)), 3)
        pygame.draw.circle(game_window.surface, (255, 255, 255), (int(pos_x), int(pos_y)), 3)

        self.x = pos_x
        self.y = pos_y

    def add_force(self,delta_x,delta_y):
        self.dx += delta_x
        self.dy += delta_y

    def move_once(self,game_window):
        tempx = self.x + (self.dx/self.mass)
        tempy = self.y + (self.dy/self.mass)
        self.move_to(game_window,tempx,tempy)

#opened for testing
if __name__=='__main__':
    pygame.init()
    window = Game_Window(1000,1000)
    window.update()
    fps_clock = pygame.time.Clock()
    fps_limit = 60
    pygame.draw.circle(window.surface,(255,255,255),(500,500),3)

    mars = Planet(window, 1, 500, 550)
    mars.add_force(0.9,-0.6)

    earth = Planet(window,80,500,500)
    earth.add_force(-0.6, 0.6)


    while 1:
        force = physics.gravity_force(mars,earth)

        mars.add_force(*force)
        earth.add_force(-force[0],-force[1])
        earth.move_once(window)
        mars.move_once(window)
        pygame.display.update()


        fps_clock.tick(fps_limit)


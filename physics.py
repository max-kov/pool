import math,pygame

class Planet():
    def __init__(self, game_window, planet_mass, planet_x, planet_y, *args):
        self.mass = planet_mass
        self.x = planet_x
        self.y = planet_y
        self.dx = 0
        self.dy = 0
        self.size = planet_mass**0.3

    def move_to(self,game_window,pos_x,pos_y):
        pygame.draw.circle(game_window.surface, (0,0,0), (int(self.x), int(self.y)), int(self.size))
        pygame.draw.circle(game_window.surface, (255, 255, 255), (int(pos_x), int(pos_y)), int(self.size))

        self.x = pos_x
        self.y = pos_y

    def add_force(self,delta_x,delta_y):
        self.dx += delta_x
        self.dy += delta_y

    def move_once(self,game_window):
        tempx = self.x + (self.dx/self.mass)
        tempy = self.y + (self.dy/self.mass)
        self.move_to(game_window,tempx,tempy)

    def merge(self,planet):
        self.x = planet.x
        self.y = planet.y
        self.dx = 0
        self.dy = 0
        self.mass += planet.mass
        self.size = self.mass**0.3


def planet_distance(pl1,pl2):
    # using pythaoreas to calculate the range between planets
    dist_x = (pl1.x-pl2.x)
    dist_y = (pl1.y-pl2.y)
    return math.sqrt(dist_x**2 + dist_y**2)

#works only in one dimension
def gravity_force(pl1,pl2):
    dist_x = (pl1.x-pl2.x)
    dist_y = (pl1.y-pl2.y)
    dist = planet_distance(pl1,pl2)
    #using newtonian model for gravitational attraction
    try:
        #dist = 0
        force = (pl1.mass*pl2.mass)/(dist**2)
        force_x = force*(dist_x/dist)
        force_y = force*(dist_y/dist)
        return -force_x, -force_y
    except:
        return 0
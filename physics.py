import math, pygame


class Planet():
    def __init__(self, planet_mass, planet_x, planet_y, **kwargs):
        self.mass = planet_mass
        self.x = planet_x
        self.y = planet_y
        self.dx = 0
        self.dy = 0
        self.not_moveable = False
        self.is_bouncy = False

        for key in kwargs:
            if key == "is_moveable":
                self.not_moveable = kwargs[key]
            if key == "is_bouncy":
                self.is_bouncy = kwargs[key]

        if self.is_bouncy:
            self.size = planet_mass
        else:
            self.size = planet_mass ** 0.3


    def move_to(self, game_window, pos_x, pos_y):

        pygame.draw.circle(game_window.surface, (0, 0, 0), (int(self.x), int(self.y)), int(self.size))
        pygame.draw.circle(game_window.surface, (255, 255, 255), (int(pos_x), int(pos_y)), int(self.size))

        self.x = pos_x
        self.y = pos_y

    def add_force(self, delta_x, delta_y):
        if not self.not_moveable:
            self.dx += delta_x
            self.dy += delta_y

    def move_once(self, game_window):
        tempx = self.x + (self.dx / self.mass)
        tempy = self.y + (self.dy / self.mass)
        self.move_to(game_window, tempx, tempy)

    def merge(self, planet):
        if not self.not_moveable:
            self.dx += (planet.dx * (planet.mass / 100)) / self.mass
            self.dy += (planet.dy * (planet.mass / 100)) / self.mass
        self.mass += planet.mass
        self.size = self.mass ** 0.3


    def set_vector(self, delta_x, delta_y):
        self.dx = delta_x
        self.dy = delta_y

def planet_distance(pl1, pl2):
    # using pythaoreas to calculate the range between planets
    dist_x = (pl1.x - pl2.x)
    dist_y = (pl1.y - pl2.y)
    return math.sqrt(dist_x ** 2 + dist_y ** 2)

def collide_bouncy(pl1,pl2):
    # a detailed explanation of how resultant vectors of ball collision is derived

    # first ve get the distance difference vector - a vector from one centre of the ball to the other ball
    # p value can be derived if you start out with the law of conservation of momentum (m1 = m1' +dmomentum ; m2 = m2' - momentum)
    # then break down any change in momentum into a normalised vector (n_vector) and a scalar
    # devide the whole thing by masses to get v1' = v1+(scalar/mass1)*n_vector
    # we can now get the new movement vector if we get the scalar a.k.a p_value
    # to get the p_value you need to use the fact that any vector can be derived from any sum of one vector and another,
    # perpendicular to it, so if we need to get a vector perpendicular to vector N, to describe the resultant vector
    # the you need to use the law of conservation of energy, kinetic energy with vector values to be exact. Then
    # substitute the vector values to sums of vector n and the one perpendicular to it. At that point an equation can be
    # derived with only one unknown - p_value



    dist = planet_distance(pl1,pl2)
    #calculating normalised (sub 1 values) difference vector
    nx = (pl1.x-pl2.x) / dist
    ny = (pl1.y-pl2.y) / dist
    #calculating the p value
    p =  2*(pl1.dx*nx + pl1.dy*ny - pl2.dx * nx - pl2.dy * ny)/(pl1.mass+pl2.mass)
    resultant_x1 = pl1.dx - p * pl1.mass * nx
    resultant_y1 = pl1.dy - p * pl1.mass * ny
    resultant_x2 = pl2.dx + p * pl2.mass * nx
    resultant_y2 = pl2.dy + p * pl2.mass * ny

    pl1.set_vector(resultant_x1,resultant_y1)
    pl2.set_vector(resultant_x2,resultant_y2)


def gravity_force(pl1, pl2):
    dist_x = (pl1.x - pl2.x)
    dist_y = (pl1.y - pl2.y)
    dist = planet_distance(pl1, pl2)
    # using newtonian model for gravitational attraction
    try:
        # dist = 0 div error
        force = ((pl1.mass * pl2.mass) / (dist ** 2)) / 2
        force_x = force * (dist_x / dist)
        force_y = force * (dist_y / dist)
        return -force_x, -force_y
    except:
        return 0

def direction_test(pl1,pl2):

    if (pl1.dx>=0 and pl2.dx>=0) or (pl1.dx<=0 and pl2.dx<=0):
        if (pl1.dy>=0 and pl2.dy>=0) or (pl1.dy<=0 and pl2.dy<=0):
            return True
    else:
        return False
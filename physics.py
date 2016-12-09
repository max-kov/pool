import math, pygame
import main


class Planet():
    def __init__(self, ball_mass, planet_x, planet_y):
        self.mass = ball_mass
        self.x = planet_x
        self.y = planet_y
        self.dx = 0
        self.dy = 0

        self.size = ball_mass

    def move_to(self, pos_x, pos_y):
        pygame.draw.circle(main.window.surface, (0, 100, 0), (int(self.x), int(self.y)), int(self.size))
        pygame.draw.circle(main.window.surface, (255, 255, 255), (int(pos_x), int(pos_y)), int(self.size))

        self.x = pos_x
        self.y = pos_y

    def add_force(self, delta_x, delta_y):
        self.dx += delta_x / self.mass
        self.dy += delta_y / self.mass

    def move_once(self, scale=1):
        tempx = self.x + self.dx*scale
        tempy = self.y + self.dy*scale
        self.move_to(tempx, tempy)

    def set_vector(self, delta_x, delta_y):
        self.dx = delta_x
        self.dy = delta_y


def ball_distance(ball1, ball2):
    # using pythaoreas to calculate the range between planets
    dist_x = (ball1.x - ball2.x)
    dist_y = (ball1.y - ball2.y)
    return math.sqrt(dist_x ** 2 + dist_y ** 2)


def distance_test(ball1, ball2, distance):
    # comparing distance without using square root to improve accuracy and speed

    dist_x = (ball1.x - ball2.x)
    dist_y = (ball1.y - ball2.y)

    if distance ** 2 <= (dist_x ** 2 + dist_y ** 2):
        return False
    else:
        return True


def normalise_vector(x, y, magnitude):
    try:
        nx = x / magnitude
        ny = y / magnitude
    except:
        # division by 0
        return 0, 0
    else:
        return nx, ny


def collide_balls(pl1,pl2):
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



    dist = ball_distance(pl1,pl2)
    #calculating normalised (sub 1 values) difference vector
    nx, ny = normalise_vector((pl1.x-pl2.x),(pl1.y-pl2.y),dist)

    #calculating the p value
    p =  2*(pl1.dx*nx + pl1.dy*ny - pl2.dx * nx - pl2.dy * ny)/(pl1.mass+pl2.mass)
    resultant_x1 = (pl1.dx - p * pl2.mass * nx)
    resultant_y1 = (pl1.dy - p * pl2.mass * ny)
    resultant_x2 = (pl2.dx + p * pl1.mass * nx)
    resultant_y2 = (pl2.dy + p * pl1.mass * ny)

    pl1.set_vector(resultant_x1,resultant_y1)
    pl2.set_vector(resultant_x2,resultant_y2)

    next_x_1 = pl1.x + resultant_x1
    next_y_1 = pl1.y + resultant_y1
    next_x_2 = pl2.x + resultant_x2
    next_y_2 = pl2.y + resultant_y2

    next_dist = math.sqrt((next_x_1 - next_x_2)**2 + (next_y_1 - next_y_2)**2)-pl1.size-pl2.size

    if (next_dist<=0):
        #checks if in the next frames the blass will be inside each other
        #and if they are moves them away using normalised difference vector
        next_dist = -1*next_dist
        fixed_x_1 = pl1.x + nx * (next_dist / 2)
        fixed_y_1 = pl1.y + ny * (next_dist / 2)
        fixed_x_2 = pl2.x - nx * (next_dist / 2)
        fixed_y_2 = pl2.y - ny * (next_dist / 2)

        pl1.move_to(fixed_x_1,fixed_y_1)
        pl2.move_to(fixed_x_2, fixed_y_2)

def perfect_break(pl1,pl2,pl3):
    dist = ball_distance(pl1,pl2)
    #calculating normalised (sub 1 values) difference vector
    nx, ny = normalise_vector((pl1.x-pl2.x),(pl1.y-pl2.y),dist)

    #calculating the p value
    p =  2*(pl1.dx*nx + pl1.dy*ny - pl2.dx * nx - pl2.dy * ny)/(pl1.mass+pl2.mass)
    resultant_x1 = (pl1.dx - p * pl2.mass * nx)
    resultant_y1 = (pl1.dy - p * pl2.mass * ny)
    resultant_x2 = (pl2.dx + p * pl1.mass * nx)
    resultant_y2 = (pl2.dy + p * pl1.mass * ny)

    pl1.set_vector(-pl1.dx, -pl1.dy)
    pl2.set_vector(resultant_x2,resultant_y2)
    pl3.set_vector(resultant_x2, -resultant_y2)

    next_x_1 = pl1.x + resultant_x1
    next_y_1 = pl1.y + resultant_y1
    next_x_2 = pl2.x + resultant_x2
    next_y_2 = pl2.y + resultant_y2

    next_dist = math.sqrt((next_x_1 - next_x_2)**2 + (next_y_1 - next_y_2)**2)-pl1.size-pl2.size

    if (next_dist<=0):
        #checks if in the next frames the blass will be inside each other
        #and if they are moves them away using normalised difference vector
        next_dist = -1*next_dist
        fixed_x_1 = pl1.x + nx * (next_dist / 2)
        fixed_y_1 = pl1.y + ny * (next_dist / 2)
        fixed_x_2 = pl2.x - nx * (next_dist / 2)
        fixed_y_2 = pl2.y - ny * (next_dist / 2)

        pl1.move_to(fixed_x_1,fixed_y_1)
        pl2.move_to(fixed_x_2, fixed_y_2)


def collision_test(pl1,pl2):
    target_vector_x1 = pl2.x - pl1.x
    target_vector_y1 = pl2.y - pl1.y
    vector_difference_x = pl1.dx - pl2.dx
    vector_difference_y = pl1.dy - pl2.dy

    if distance_test(pl1,pl2,pl1.size+pl2.size-0.1):
        if (pl1.dx==0 and pl1.dy==0) and (pl2.dx==0 and pl2.dy==0):
            return False
        else:
            #checks if the balls can collide considering their direction and speed
            if target_vector_x1*vector_difference_x>0 or target_vector_y1*vector_difference_y>0:
                return True
            else:
                return False
    else:
        return False

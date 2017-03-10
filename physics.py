import math
import numpy as np

def ball_distance(ball1, ball2):
    # using pythaoreas to calculate the range between ballanets
    return np.linalg.norm(ball1.pos-ball2.pos)

def point_distance(p1,p2):
    dist_x = (p1[0] - p2[0])
    dist_y = (p1[1] - p2[1])
    return math.sqrt(dist_x ** 2 + dist_y ** 2)


def distance_test(x1,y1, x2,y2, distance):
    # comparing distance without using square root to improve accuracy and speed

    dist_x = (x1 - x2)
    dist_y = (y1 - y2)

    return not distance ** 2 <= (dist_x ** 2 + dist_y ** 2)

def normalise_vector(x, y, magnitude):
    try:
        nx = x / magnitude
        ny = y / magnitude
    except:
        # division by 0
        return 0, 0
    else:
        return nx, ny


def collide_balls(game_state, ball1, ball2):

    dist = ball_distance(ball1, ball2)
    #calculating normalised (sub 1 values) difference vector
    nx, ny = normalise_vector((ball1.pos[0] - ball2.pos[0]), (ball1.pos[1] - ball2.pos[1]), dist)

    #calculating the momentum difference
    p =  2*(ball1.velocity[0] * nx + ball1.velocity[1] * ny - ball2.velocity[0] * nx - ball2.velocity[1] * ny) / (ball1.mass + ball2.mass)
    resultant_x1 = (ball1.velocity[0] - p * ball2.mass * nx)
    resultant_y1 = (ball1.velocity[1] - p * ball2.mass * ny)
    resultant_x2 = (ball2.velocity[0] + p * ball1.mass * nx)
    resultant_y2 = (ball2.velocity[1] + p * ball1.mass * ny)

    ball1.set_vector(resultant_x1, resultant_y1)
    ball2.set_vector(resultant_x2, resultant_y2)

    next_x_1 = ball1.pos[0] + resultant_x1
    next_y_1 = ball1.pos[1] + resultant_y1
    next_x_2 = ball2.pos[0] + resultant_x2
    next_y_2 = ball2.pos[1] + resultant_y2

    next_dist = math.sqrt((next_x_1 - next_x_2)**2 + (next_y_1 - next_y_2)**2) - ball1.radius - ball2.radius

    if (next_dist<=0):
        #checks if in the next frames the blass will be inside each other
        #and if they are moves them away using normalised difference vector
        next_dist = -1*next_dist
        fixed_x_1 = ball1.pos[0] + nx * (next_dist / 2)
        fixed_y_1 = ball1.pos[1] + ny * (next_dist / 2)
        fixed_x_2 = ball2.pos[0] - nx * (next_dist / 2)
        fixed_y_2 = ball2.pos[1] - ny * (next_dist / 2)

        ball1.move_to(game_state, fixed_x_1, fixed_y_1)
        ball2.move_to(game_state, fixed_x_2, fixed_y_2)

def perfect_break(game_state, ball1, ball2, ball3):
    dist = ball_distance(ball1, ball2)
    #calculating normalised (sub 1 values) difference vector
    nx, ny = normalise_vector((ball1.pos[0] - ball2.pos[0]), (ball1.pos[1] - ball2.pos[1]), dist)
    #calculating the p value
    p =  2*(ball1.velocity[0] * nx + ball1.velocity[1] * ny - ball2.velocity[0] * nx - ball2.velocity[1] * ny) / (ball1.mass + ball2.mass)
    resultant_x1 = (ball1.velocity[0] - p * ball2.mass * nx)
    resultant_y1 = (ball1.velocity[1] - p * ball2.mass * ny)
    resultant_x2 = (ball2.velocity[0] + p * ball1.mass * nx)
    resultant_y2 = (ball2.velocity[1] + p * ball1.mass * ny)

    ball1.set_vector(-ball1.velocity[0], -ball1.velocity[1])
    ball2.set_vector(resultant_x2, resultant_y2)
    ball3.set_vector(resultant_x2, -resultant_y2)

    next_x_1 = ball1.pos[0] + resultant_x1
    next_y_1 = ball1.pos[1] + resultant_y1
    next_x_2 = ball2.pos[0] + resultant_x2
    next_y_2 = ball2.pos[1] + resultant_y2

    next_dist = math.sqrt((next_x_1 - next_x_2)**2 + (next_y_1 - next_y_2)**2) - ball1.radius - ball2.radius

    if (next_dist<=0):
        #checks if in the next frames the blass will be inside each other
        #and if they are moves them away using normalised difference vector
        next_dist = -1*next_dist
        fixed_x_1 = ball1.pos[0] + nx * (next_dist / 2)
        fixed_y_1 = ball1.pos[1] + ny * (next_dist / 2)
        fixed_x_2 = ball2.pos[0] - nx * (next_dist / 2)
        fixed_y_2 = ball2.pos[1] - ny * (next_dist / 2)

        ball1.move_to(game_state, fixed_x_1, fixed_y_1)
        ball2.move_to(game_state, fixed_x_2, fixed_y_2)


def collision_test(ball1, ball2):

    return np.linalg.norm(ball1.pos-ball2.pos)<ball1.radius+ball2.radius


def triangle_area(side1,side2,side3):
    # herons formula
    half_perimetre = abs((side1+side2+side3)*0.5)
    return math.sqrt(half_perimetre*(half_perimetre-abs(side1))*(half_perimetre-abs(side2))*(half_perimetre-abs(side3)))
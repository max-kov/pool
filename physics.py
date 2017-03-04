import math

def ball_distance(ball1, ball2):
    # using pythaoreas to calculate the range between planets
    dist_x = (ball1.x - ball2.x)
    dist_y = (ball1.y - ball2.y)
    return math.sqrt(dist_x ** 2 + dist_y ** 2)

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


def collide_balls(game_state, pl1, pl2):

    dist = ball_distance(pl1,pl2)
    #calculating normalised (sub 1 values) difference vector
    nx, ny = normalise_vector((pl1.x-pl2.x),(pl1.y-pl2.y),dist)

    #calculating the momentum difference
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

    next_dist = math.sqrt((next_x_1 - next_x_2)**2 + (next_y_1 - next_y_2)**2)-pl1.radius-pl2.radius

    if (next_dist<=0):
        #checks if in the next frames the blass will be inside each other
        #and if they are moves them away using normalised difference vector
        next_dist = -1*next_dist
        fixed_x_1 = pl1.x + nx * (next_dist / 2)
        fixed_y_1 = pl1.y + ny * (next_dist / 2)
        fixed_x_2 = pl2.x - nx * (next_dist / 2)
        fixed_y_2 = pl2.y - ny * (next_dist / 2)

        pl1.move_to(game_state, fixed_x_1, fixed_y_1)
        pl2.move_to(game_state, fixed_x_2, fixed_y_2)

def perfect_break(game_state, pl1, pl2, pl3):
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

    next_dist = math.sqrt((next_x_1 - next_x_2)**2 + (next_y_1 - next_y_2)**2)-pl1.radius-pl2.radius

    if (next_dist<=0):
        #checks if in the next frames the blass will be inside each other
        #and if they are moves them away using normalised difference vector
        next_dist = -1*next_dist
        fixed_x_1 = pl1.x + nx * (next_dist / 2)
        fixed_y_1 = pl1.y + ny * (next_dist / 2)
        fixed_x_2 = pl2.x - nx * (next_dist / 2)
        fixed_y_2 = pl2.y - ny * (next_dist / 2)

        pl1.move_to(game_state, fixed_x_1, fixed_y_1)
        pl2.move_to(game_state, fixed_x_2, fixed_y_2)


def collision_test(pl1,pl2):
    target_vector_x1 = pl2.x - pl1.x
    target_vector_y1 = pl2.y - pl1.y
    vector_difference_x = pl1.dx - pl2.dx
    vector_difference_y = pl1.dy - pl2.dy

    if distance_test(pl1.x,pl1.y,pl2.x,pl2.y,pl1.radius+pl2.radius-0.1):
        if (pl1.dx==0 and pl1.dy==0) and (pl2.dx==0 and pl2.dy==0):
            return False
        else:
            #checks if the balls can collide considering their direction and speed
            return target_vector_x1*vector_difference_x>0 or target_vector_y1*vector_difference_y>0
    else:
        return False

def triangle_area(side1,side2,side3):
    # herons formula
    half_perimetre = abs((side1+side2+side3)*0.5)
    return math.sqrt(half_perimetre*(half_perimetre-abs(side1))*(half_perimetre-abs(side2))*(half_perimetre-abs(side3)))
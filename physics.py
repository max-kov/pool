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


def collide_balls(ball1, ball2):

    point_diff = ball2.pos-ball1.pos
    system_velocity = ball1.velocity-ball2.velocity
    # hack to avoid dy or dx =0
    system_velocity+=0.001
    dist = np.linalg.norm(point_diff)

    if np.dot(point_diff,system_velocity)>0:
        collision = point_diff/dist
        ball1_dot = np.dot(ball1.velocity,collision)
        ball2_dot = np.dot(ball2.velocity,collision)

        ball1.velocity += (ball2_dot-ball1_dot)*collision
        ball2.velocity += (ball1_dot-ball2_dot)*collision


def collision_test(ball1, ball2):
    return (ball_distance(ball1,ball2)<ball1.radius+ball2.radius) and \
           np.count_nonzero(ball1.velocity+ball2.velocity)>0


def triangle_area(side1,side2,side3):
    # herons formula
    half_perimetre = abs((side1+side2+side3)*0.5)
    return math.sqrt(half_perimetre*(half_perimetre-abs(side1))*(half_perimetre-abs(side2))*(half_perimetre-abs(side3)))
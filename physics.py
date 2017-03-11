import math
import numpy as np


def point_distance(p1, p2):
    dist_diff = p1-p2
    return np.hypot(dist_diff[0],dist_diff[1])


def collide_balls(ball1, ball2):
    point_diff = ball2.pos - ball1.pos
    system_velocity = ball1.velocity - ball2.velocity
    # hack to avoid dy or dx =0 , 0.001 is negligible
    system_velocity += 0.001
    dist = point_distance(ball1.pos,ball2.pos)

    if np.dot(point_diff, system_velocity) > 0:
        collision = point_diff / dist
        ball1_dot = np.dot(ball1.velocity, collision)
        ball2_dot = np.dot(ball2.velocity, collision)

        ball1.velocity += (ball2_dot - ball1_dot) * collision
        ball2.velocity += (ball1_dot - ball2_dot) * collision


def collision_test(ball1, ball2):
    return (point_distance(ball1.pos, ball2.pos) < ball1.radius + ball2.radius) and \
           np.count_nonzero(ball1.velocity + ball2.velocity) > 0


def triangle_area(side1, side2, side3):
    # herons formula
    half_perimetre = abs((side1 + side2 + side3) * 0.5)
    try:
        return math.sqrt(half_perimetre * (half_perimetre - abs(side1)) * (half_perimetre - abs(side2)) * (half_perimetre - abs(side3)))
    except:
        # not a triangle
        return 0

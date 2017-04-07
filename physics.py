import math
import numpy as np


def point_distance(p1, p2):
    dist_diff = p1 - p2
    return np.hypot(*dist_diff)


def collide_balls(ball1, ball2):
    point_diff = ball2.pos - ball1.pos
    system_velocity = ball1.velocity - ball2.velocity
    dist = point_distance(ball1.pos, ball2.pos)

    # checks vector projections to determine is 2 balls are moving toward each other
    if np.dot(point_diff, system_velocity) >= 0:
        collision = point_diff / dist
        ball1_dot = np.dot(ball1.velocity, collision)
        ball2_dot = np.dot(ball2.velocity, collision)

        ball1.add_force((ball2_dot - ball1_dot) * collision * ball1.mass)
        ball2.add_force((ball1_dot - ball2_dot) * collision * ball2.mass)


def collision_test(ball1, ball2):
    # checks distance and if both balls are stationary
    return (point_distance(ball1.pos, ball2.pos) < ball1.radius + ball2.radius) and \
           np.count_nonzero(np.concatenate((ball1.velocity, ball2.velocity))) > 0


def triangle_area(side1, side2, side3):
    # herons formula
    half_perimetre = abs((side1 + side2 + side3) * 0.5)
    try:
        return math.sqrt(half_perimetre * (half_perimetre - abs(side1)) * (half_perimetre - abs(side2)) * (
        half_perimetre - abs(side3)))
    except:
        # not a triangle
        return 0


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

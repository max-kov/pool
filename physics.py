import math
import numpy as np


def point_distance(p1, p2):
    dist_diff = p1 - p2
    return np.hypot(*dist_diff)


def collide_balls(ball1, ball2):
    point_diff = ball2.pos - ball1.pos
    dist = point_distance(ball1.pos, ball2.pos)
    # normalising circle distance difference vector
    collision = point_diff / dist
    # projecting balls velocity ONTO difference vector
    ball1_dot = np.dot(ball1.velocity, collision)
    ball2_dot = np.dot(ball2.velocity, collision)
    # since the masses of the balls are the same, the velocity will just switch
    ball1.velocity += (ball2_dot - ball1_dot) * collision
    ball2.velocity += (ball1_dot - ball2_dot) * collision


def collision_test(ball1, ball2):
    # distance check followed by checking if either of the balls are moving
    # followed by vector projection check, to see if both are moving towards each other
    return (point_distance(ball1.pos, ball2.pos) < ball1.radius + ball2.radius) and \
           np.count_nonzero(np.concatenate((ball1.velocity, ball2.velocity))) > 0 and \
           np.dot(ball2.pos - ball1.pos, ball1.velocity - ball2.velocity) >= 0


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


def line_collision(line_points, ball):
    # displacement vector from the first point to the ball
    displacement_to_ball = ball.pos - line_points[0]
    # displacement vector from the first point to the second point on the line
    displacement_to_second_point = line_points[1] - line_points[0]
    normalised_point_diff_vector = displacement_to_second_point / np.hypot(*(displacement_to_second_point))
    # distance from the first point on the line projected onto point displacement vector
    projected_distance = np.dot(normalised_point_diff_vector, displacement_to_ball)
    # closest point on the line to the ball
    closest_line_point = projected_distance * normalised_point_diff_vector
    perpendicular_vector = np.array([-normalised_point_diff_vector[1], normalised_point_diff_vector[0]])
    # checking if closest point on the line is actually on the line (which is not always the case when projecting)
    # and checking if the distance from that point to the ball is less than the balls radius
    if -ball.radius < projected_distance < np.hypot(*(displacement_to_second_point)) + ball.radius and \
                    np.hypot(*(closest_line_point - ball.pos + line_points[0])) <= ball.radius and \
                    np.dot(perpendicular_vector, ball.velocity) <= 0:
        ball.velocity -= 2 * np.dot(perpendicular_vector, ball.velocity) * perpendicular_vector

import math

import numpy as np

import config


def point_distance(p1, p2):
    dist_diff = p1 - p2
    return np.hypot(*dist_diff)


def distance_less_equal(p1, p2, dist):
    # does distance comparisons without calculating square roots
    dist_diff = p1 - p2
    return (dist_diff[0] ** 2 + dist_diff[1] ** 2) <= dist ** 2


def ball_collision_check(ball1, ball2):
    # distance check followed by checking if either of the balls are moving
    # followed by vector projection check, to see if both are moving towards
    # each other
    return distance_less_equal(ball1.pos, ball2.pos, 2 * config.ball_radius) and \
           np.count_nonzero(np.concatenate((ball1.velocity, ball2.velocity))) > 0 and \
           np.dot(ball2.pos - ball1.pos, ball1.velocity - ball2.velocity) > 0


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


def triangle_area(side1, side2, side3):
    # used to determine if the user is clicking on the cue stick
    # herons formula
    half_perimetre = abs((side1 + side2 + side3) * 0.5)
    return math.sqrt(half_perimetre * (half_perimetre - abs(side1)) * (half_perimetre - abs(side2)) * (
            half_perimetre - abs(side3)))


def rotation_matrix(axis, theta):
    # Return the rotation matrix associated with counterclockwise rotation about
    # the given axis by theta radians.
    axis = np.asarray(axis)
    axis = axis / math.sqrt(np.dot(axis, axis))
    a = math.cos(theta / 2.0)
    b, c, d = -axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])


def line_ball_collision_check(line, ball):
    # checks if the ball is half the line length from the line middle
    if distance_less_equal(line.middle, ball.pos, line.length / 2 + config.ball_radius):
        # displacement vector from the first point to the ball
        displacement_to_ball = ball.pos - line.line[0]
        # displacement vector from the first point to the second point on the
        # line
        displacement_to_second_point = line.line[1] - line.line[0]
        normalised_point_diff_vector = displacement_to_second_point / \
                                       np.hypot(*(displacement_to_second_point))
        # distance from the first point on the line to the perpendicular
        # projection point from the ball
        projected_distance = np.dot(normalised_point_diff_vector, displacement_to_ball)
        # closest point on the line to the ball
        closest_line_point = projected_distance * normalised_point_diff_vector
        perpendicular_vector = np.array(
            [-normalised_point_diff_vector[1], normalised_point_diff_vector[0]])
        # checking if closest point on the line is actually on the line (which is not always the case when projecting)
        # then checking if the distance from that point to the ball is less than the balls radius and finally
        # checking if the ball is moving towards the line with the dot product
        return -config.ball_radius / 3 <= projected_distance <= \
               np.hypot(*(displacement_to_second_point)) + config.ball_radius / 3 and \
               np.hypot(*(closest_line_point - ball.pos + line.line[0])) <= \
               config.ball_radius and np.dot(
            perpendicular_vector, ball.velocity) <= 0


def collide_line_ball(line, ball):
    displacement_to_second_point = line.line[1] - line.line[0]
    normalised_point_diff_vector = displacement_to_second_point / \
                                   np.hypot(*(displacement_to_second_point))
    perpendicular_vector = np.array(
        [-normalised_point_diff_vector[1], normalised_point_diff_vector[0]])
    ball.velocity -= 2 * np.dot(perpendicular_vector,
                                ball.velocity) * perpendicular_vector

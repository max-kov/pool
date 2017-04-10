import itertools
import pygame

import physics


def table_collision(game_state):
    def ball_to_hole_collision(ball, hole):
        return physics.point_distance(ball.pos, hole.pos) - hole.radius <= 0

    # destroys any circles that are in a hole
    pygame.sprite.groupcollide(game_state.balls, game_state.holes, True, False, ball_to_hole_collision)

    for triangle in game_state.table_sides:
        for ball in game_state.balls:
            physics.line_collision(triangle.line, ball)

def check_for_collision(game_state):
    table_collision(game_state)

    collided = True
    while collided:
        collided = False
        for combination in itertools.combinations(game_state.balls, 2):
            if physics.collision_check(*combination):
                physics.collide_balls(*combination)
                collided = True

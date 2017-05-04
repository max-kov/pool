import itertools
import pygame
import random

import physics
from config import hole_radius


def resolve_collisions(game_state):
    def ball_hole_collision_check(ball, hole):
        return physics.point_distance(ball.pos, hole.pos) - hole_radius <= 0

    # destroys any circles that are in a hole
    pygame.sprite.groupcollide(
        game_state.balls, game_state.holes, True, False, ball_hole_collision_check)

    for line_ball_combination in itertools.product(game_state.table_sides, game_state.balls):
        if physics.line_ball_collision_check(*line_ball_combination):
            physics.collide_line_ball(*line_ball_combination)

    ball_list = game_state.balls.sprites()
    # ball list is shuffled to randomize ball collisions on the 1st break
    random.shuffle(ball_list)

    for ball_combination in itertools.combinations(ball_list, 2):
        if physics.ball_collision_check(*ball_combination):
            physics.collide_balls(*ball_combination)

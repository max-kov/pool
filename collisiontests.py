import itertools
import random

import pygame

import config
import physics


def resolve_all_collisions(game_state):
    def ball_hole_collision_check(ball, hole):
        if physics.distance_less_equal(ball.pos, hole.pos, config.hole_radius):
            game_state.potted.append(ball.number)
            # need to redraw table coloring to avoid ball shift glitch
            game_state.table_coloring.refresh()
            return True
        else:
            return False

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
            # remembers which type of the ball the white ball hit first
            if (ball_combination[0].number == 0 or ball_combination[1].number == 0) and \
                    not game_state.white_ball_1st_hit_is_set:
                game_state.white_ball_1st_hit_is_set = True
                if ball_combination[0].number == 0:
                    game_state.white_ball_1st_hit_is_stripes = ball_combination[1].is_striped
                else:
                    game_state.white_ball_1st_hit_is_stripes = ball_combination[0].is_striped


def check_if_ball_touches_balls(target_ball_pos, target_ball_number, game_state):
    touches_other_balls = False
    for ball in game_state.balls:
        if target_ball_number != ball.number and \
                physics.distance_less_equal(ball.pos, target_ball_pos, config.ball_radius * 2):
            touches_other_balls = True
            break
    return touches_other_balls

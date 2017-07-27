import itertools
import random

import pygame
import zope.event

import config
import event
import physics


def resolve_all_collisions(balls, holes, table_sides):
    def ball_hole_collision_check(ball, hole):
        if physics.distance_less_equal(ball.ball.pos, hole.pos, config.hole_radius):
            zope.event.notify(event.GameEvent("POTTED", ball))
            return True
        else:
            return False

    # destroys any circles that are in a hole
    pygame.sprite.groupcollide(
        balls, holes, True, False, ball_hole_collision_check)

    for line_ball_combination in itertools.product(table_sides, balls):
        if physics.line_ball_collision_check(line_ball_combination[0], line_ball_combination[1].ball):
            physics.collide_line_ball(line_ball_combination[0], line_ball_combination[1].ball)

    ball_list = balls.sprites()
    # ball list is shuffled to randomize ball collisions on the 1st break
    random.shuffle(ball_list)

    for ball_combination in itertools.combinations(ball_list, 2):
        if physics.ball_collision_check(ball_combination[0].ball, ball_combination[1].ball):
            physics.collide_balls(ball_combination[0].ball, ball_combination[1].ball)
            zope.event.notify(event.GameEvent("COLLISION", ball_combination))

def check_if_ball_touches_balls(target_ball_pos, target_ball_number, game_state):
    touches_other_balls = False
    for ball in game_state.balls:
        if target_ball_number != ball.number and \
                physics.distance_less_equal(ball.pos, target_ball_pos, config.ball_radius * 2):
            touches_other_balls = True
            break
    return touches_other_balls

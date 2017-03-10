import physics
import pygame


def ball_to_hole_collision(ball, hole):
    return physics.distance_test(ball.pos[0], ball.pos[1], hole.x, hole.y, hole.radius)


def table_collision(game_state):
    # destroys any circles that are in a hole
    pygame.sprite.groupcollide(game_state.balls, game_state.holes, True, False, ball_to_hole_collision)

    for i, side in enumerate(game_state.sides):
        ball = pygame.sprite.spritecollideany(side, game_state.balls)
        if not (ball == None):
            side.ball_hit(ball)


def check_for_collision(game_state):
    table_collision(game_state)

    balls = game_state.balls
    balls_to_delete = []
    for counter1, ball1 in enumerate(balls):
        for counter2, ball2 in enumerate(balls):
            if not counter1 == counter2:
                if physics.collision_test(ball1, ball2):
                    physics.collide_balls(ball1,ball2)

    for ball in balls_to_delete:
        balls[ball].destroy(game_state)
        balls.pop(ball)

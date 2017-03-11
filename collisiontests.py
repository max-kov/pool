import physics
import pygame


def table_collision(game_state):
    def ball_to_hole_collision(ball, hole):
        return physics.point_distance(ball.pos, hole.pos) - hole.radius <= 0

    # destroys any circles that are in a hole
    pygame.sprite.groupcollide(game_state.balls, game_state.holes, True, False, ball_to_hole_collision)

    for i, side in enumerate(game_state.sides):
        ball = pygame.sprite.spritecollideany(side, game_state.balls)
        if ball is not None:
            side.ball_hit(ball)


def check_for_collision(game_state):
    table_collision(game_state)

    balls = game_state.balls
    for counter1, ball1 in enumerate(balls):
        for counter2, ball2 in enumerate(balls):
            if not counter1 == counter2:
                if physics.collision_test(ball1, ball2):
                    physics.collide_balls(ball1, ball2)

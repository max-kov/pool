import physics
import pygame

def table_collision(game_state):
    # destroys any circles that are in a hole
    pygame.sprite.groupcollide (game_state.balls, game_state.holes, True, False)

    for i, side in enumerate(game_state.sides):
        ball = pygame.sprite.spritecollideany(side, game_state.balls)
        if not (ball==None):
            side.ball_hit(ball)


def check_for_collision(game_state):
    table_collision(game_state)

    balls = game_state.balls
    balls_to_delete = []
    for counter1, ball1 in enumerate(balls):
        collision_list = []
        for counter2, ball2 in enumerate(balls):
            if not counter1 == counter2:
                if physics.collision_test(ball1, ball2):
                    collision_list.append(ball2)

        # collided with one ball only
        if len(collision_list) <= 1:
            for index, ball in enumerate(collision_list):
                physics.collide_balls(game_state, ball1, ball)
        else:
            # collided with several balls, this will only be used at the beginning of the game
            if ball1.dy < 0:
                # collidion at a positive angle
                collision_list.reverse()
                for index, ball in enumerate(collision_list):
                    physics.collide_balls(game_state, ball1, ball)
            elif ball1.dy > 0:
                # collidion at a negative angle
                for index, ball in enumerate(collision_list):
                    physics.collide_balls(game_state, ball1, ball)
            else:
                # angle of collision = 0
                physics.perfect_break(game_state, ball1, collision_list[0], collision_list[1])


    for ball in balls_to_delete:
        balls[ball].destroy(game_state)
        balls.pop(ball)

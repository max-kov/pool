import physics


def table_collision(game_state, ball, ball_id):

    lower_x = game_state.table_margin
    upper_x = game_state.resolution[0] - game_state.table_margin
    lower_y = game_state.table_margin
    upper_y = game_state.resolution[1] - game_state.table_margin

    def is_near_table_holes():
        window_x_mid = game_state.resolution[0] / 2
        # edge holes
        if (ball.x < game_state.table_margin * 1.2 and ball.y < game_state.table_margin * 1.5) or \
                (ball.x > game_state.resolution[0] - game_state.table_margin * 1.2 and ball.y > game_state.resolution[1] - game_state.table_margin * 1.2) or \
                (ball.x < game_state.table_margin * 1.2 and ball.y > game_state.resolution[1] - game_state.table_margin * 1.2) or \
                (ball.x > game_state.resolution[0] - game_state.table_margin * 1.2 and ball.y < game_state.table_margin * 1.2):
            return True
        else:
            # midlle holes
            return (ball.x < window_x_mid + game_state.table_margin / 2 and ball.x > window_x_mid - game_state.table_margin / 2) and \
                    (ball.y > game_state.resolution[1] - game_state.table_margin or ball.y < game_state.table_margin)

    def is_hitting_sides():
        # 1st is location check
        return ball.x + ball.radius > upper_x or ball.x - ball.radius < lower_x and \
            (ball.x + ball.radius > upper_x and not ball.dx < 0) or (
            ball.x - ball.radius < lower_x and not ball.dx > 0)
        # 2nd is vector check
        # if the direction of the ball if from the wall, there is no need to change the direction


    def is_hitting_ceilings():
        return \
            (ball.y + ball.radius > upper_y or ball.y - ball.radius < lower_y) and\
        (ball.y + ball.radius > upper_y and not ball.dy < 0) or (ball.y - ball.radius < lower_y and not ball.dy > 0)


    was_deleted = False
    if not is_near_table_holes():
        if is_hitting_sides():
            # if the direction of the ball if from the wall, there is no need to change the direction
            ball.set_vector(-ball.dx, ball.dy)
        if is_hitting_ceilings():
            ball.set_vector(ball.dx, -ball.dy)

    for i, hole in enumerate(game_state.holes):
        posx = hole.x
        posy = hole.y
        if physics.distance_test(posx, posy, ball.x, ball.y, game_state.ball_size * 1.7):
            was_deleted = True
    return was_deleted


def check_for_collision(game_state):
    balls = game_state.balls
    balls_to_delete = []
    for counter1, ball1 in enumerate(balls):
        collision_list = []
        for counter2, ball2 in enumerate(balls):
            if not counter1 == counter2:
                if physics.collision_test(ball1, ball2):
                    collision_list.append(counter2)

        # collided with one ball only
        if len(collision_list) <= 1:
            for index, ballnum in enumerate(collision_list):
                physics.collide_balls(game_state, ball1, balls[ballnum])
        else:
            # collided with several balls, this will only be used at the beginning of the game
            if ball1.dy < 0:
                # collidion at a positive angle
                collision_list.reverse()
                for index, ballnum in enumerate(collision_list):
                    physics.collide_balls(game_state, ball1, balls[ballnum])
            elif ball1.dy > 0:
                # collidion at a negative angle
                for index, ballnum in enumerate(collision_list):
                    physics.collide_balls(game_state, ball1, balls[ballnum])
            else:
                # angle of collision = 0
                physics.perfect_break(game_state, ball1, balls[collision_list[0]], balls[collision_list[1]])

        if table_collision(game_state, ball1, counter1):
            balls_to_delete.append(counter1)

    for ball in balls_to_delete:
        balls[ball].destroy(game_state)
        balls.pop(ball)

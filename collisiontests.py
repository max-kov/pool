import physics


def table_collision(gameState, ball, ball_id):

    lower_x = gameState.table_margin
    upper_x = gameState.resolution[0] - gameState.table_margin
    lower_y = gameState.table_margin
    upper_y = gameState.resolution[1] - gameState.table_margin

    def is_near_table_holes():
        window_x_mid = gameState.resolution[0] / 2
        # edge holes
        if (ball.x < gameState.table_margin * 1.2 and ball.y < gameState.table_margin * 1.5) or \
                (ball.x > gameState.resolution[0] - gameState.table_margin * 1.2 and ball.y > gameState.resolution[1] - gameState.table_margin * 1.2) or \
                (ball.x < gameState.table_margin * 1.2 and ball.y > gameState.resolution[1] - gameState.table_margin * 1.2) or \
                (ball.x > gameState.resolution[0] - gameState.table_margin * 1.2 and ball.y < gameState.table_margin * 1.2):
            return True
        else:
            # midlle holes
            if (ball.x < window_x_mid + gameState.table_margin / 2 and ball.x > window_x_mid - gameState.table_margin / 2) and \
                    (ball.y > gameState.resolution[1] - gameState.table_margin or ball.y < gameState.table_margin):
                return True
            else:
                return False

    def is_hitting_sides():
        if ball.x + ball.size > upper_x or ball.x - ball.size < lower_x:
            # 1st is location check
            if (ball.x + ball.size > upper_x and not ball.dx < 0) or (
                                ball.x - ball.size < lower_x and not ball.dx > 0):
                # 2nd is vector check
                # if the direction of the ball if from the wall, there is no need to change the direction
                return True
            else:
                return False
        else:
            return False

    def is_hitting_ceilings():
        if ball.y + ball.size > upper_y or ball.y - ball.size < lower_y:
            if (ball.y + ball.size > upper_y and not ball.dy < 0) or (
                                ball.y - ball.size < lower_y and not ball.dy > 0):
                return True
            else:
                return False
        else:
            return False

    was_deleted = False
    if not is_near_table_holes():
        if is_hitting_sides():
            # if the direction of the ball if from the wall, there is no need to change the direction
            ball.set_vector(-ball.dx, ball.dy)
        if is_hitting_ceilings():
            ball.set_vector(ball.dx, -ball.dy)

    for hole in gameState.table_holes:
        posx, posy = hole
        if physics.distance_test(posx, posy, ball.x, ball.y, gameState.ball_size * 1.7):
            was_deleted = True
    return was_deleted


def check_for_collision(gameState):
    balls = gameState.balls
    balls_to_delete = []
    for counter1 in range(0, len(balls)):
        ball1 = balls[counter1]
        collision_list = []
        for counter2 in range(counter1, len(balls)):
            ball2 = balls[counter2]
            if not counter1 == counter2:
                if physics.collision_test(ball1, ball2):
                    collision_list.append(counter2)

        # collided with one ball only
        if len(collision_list) <= 1:
            for index, ballnum in enumerate(collision_list):
                physics.collide_balls(gameState,ball1, balls[ballnum])
        else:
            # collided with several balls, this will only be used at the beginning of the game
            if ball1.dy < 0:
                # collidion at a positive angle
                collision_list.reverse()
                for index, ballnum in enumerate(collision_list):
                    physics.collide_balls(gameState,ball1, balls[ballnum])
            elif ball1.dy > 0:
                # collidion at a negative angle
                for index, ballnum in enumerate(collision_list):
                    physics.collide_balls(gameState,ball1, balls[ballnum])
            else:
                # angle of collision = 0
                physics.perfect_break(gameState,ball1, balls[collision_list[0]], balls[collision_list[1]])

        if table_collision(gameState, ball1, counter1):
            balls_to_delete.append(counter1)

    for ball in balls_to_delete:
        balls[ball].destroy(gameState)
        balls.pop(ball)

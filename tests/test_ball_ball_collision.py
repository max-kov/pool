import numpy as np

from pool import ball
from pool import physics
from pool.config import ball_radius

ball1 = ball.Ball()
ball2 = ball.Ball()

ball1.move_to((0, 0))
ball1.set_velocity((1, 1))

fortyfive_degree_position = np.array(
    [np.sin(np.pi / 4), np.cos(np.pi / 4)]) * ball_radius * 2


class TestBallBallCollision():
    # distance tests will check if the ball distance collision check 
    # function is working properly

    def test_distance1(self):
        ball2.move_to((ball_radius * 2, 0))
        ball2.set_velocity((0, 0))
        assert physics.ball_collision_check(ball1, ball2)

    def test_distance2(self):
        ball2.move_to((0, ball_radius * 2 + 1))
        ball2.set_velocity((0, 0))
        assert not physics.ball_collision_check(ball1, ball2)

    def test_distance3(self):
        ball2.move_to((1, ball_radius * 2))
        ball2.set_velocity((0, 0))
        assert not physics.ball_collision_check(ball1, ball2)

    def test_distance4(self):
        ball2.move_to((ball_radius * 2 - 1, 0))
        ball2.set_velocity((0, 0))
        assert physics.ball_collision_check(ball1, ball2)

    def test_distance5(self):
        ball2.move_to((1, 0))
        ball2.set_velocity((0, 0))
        assert physics.ball_collision_check(ball1, ball2)

    def test_distance6(self):
        ball2.move_to(fortyfive_degree_position)
        ball2.set_velocity((0, 0))
        assert physics.ball_collision_check(ball1, ball2)

    # these will check that any balls that are moving away from each other
    # will not collide
    def test_movement1(self):
        ball1.set_velocity((1, 1))

        ball2.move_to((-ball_radius, 0))
        ball2.set_velocity((0, 0))
        assert not physics.ball_collision_check(ball1, ball2)

    def test_movement2(self):
        ball1.set_velocity((1, 1))

        ball2.move_to(fortyfive_degree_position)
        ball2.set_velocity((1, 1))
        assert not physics.ball_collision_check(ball1, ball2)

    def test_movement3(self):
        ball1.set_velocity((1, 1))

        ball2.move_to(fortyfive_degree_position)
        ball2.set_velocity((0.9, 1))
        assert physics.ball_collision_check(ball1, ball2)

    def test_movement4(self):
        ball1.set_velocity((1, 1))

        ball2.move_to(-fortyfive_degree_position)
        ball2.set_velocity((1, 1))
        assert not physics.ball_collision_check(ball1, ball2)

    def test_movement5(self):
        ball1.set_velocity((1, 1))

        ball2.move_to(-fortyfive_degree_position)
        ball2.set_velocity((1.1, 1))
        assert physics.ball_collision_check(ball1, ball2)

    def test_movement6(self):
        ball1.set_velocity((0, 1))

        ball2.move_to((ball_radius * 2, 0))
        ball2.set_velocity((0, 0))
        assert not physics.ball_collision_check(ball1, ball2)

    def test_movement7(self):
        ball1.set_velocity((0, 1))

        ball2.move_to((0, ball_radius * 2))
        ball2.set_velocity((200000000, 0))
        assert physics.ball_collision_check(ball1, ball2)

    def test_movement8(self):
        ball1.set_velocity((0, 1))

        ball2.move_to((0, ball_radius * 2))
        ball2.set_velocity((200000000, 0.9))
        assert physics.ball_collision_check(ball1, ball2)

    def test_movement9(self):
        ball1.set_velocity((0, 1))

        ball2.move_to((0, ball_radius * 2))
        ball2.set_velocity((200000000, 1))
        assert not physics.ball_collision_check(ball1, ball2)

    def test_movement10(self):
        ball1.set_velocity((0, 1))

        ball2.move_to((0, ball_radius * 2))
        ball2.set_velocity((200000000, -200000000000))
        assert physics.ball_collision_check(ball1, ball2)

    def test_movement11(self):
        # stationary balls do not collide to conserve unnecessary computations
        ball1.set_velocity((0, 0))

        ball2.move_to((0, ball_radius * 2))
        ball2.set_velocity((0, 0))
        assert not physics.ball_collision_check(ball1, ball2)

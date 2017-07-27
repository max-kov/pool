import itertools
import math

import numpy as np

from pool import ball
from pool import physics
from pool import table_sprites
from pool.config import ball_radius


class TestPointDistance():
    def test_point_distance1(self):
        assert physics.point_distance(np.array([0, 0]), np.array([3, 4])) == 5

    def test_point_distance2(self):
        assert physics.point_distance(
            np.array([0, -10]), np.array([0, -10])) == 0

    def test_point_distance3(self):
        assert physics.point_distance(
            np.array([10, 0]), np.array([-10, 0])) == 20


class TestTriangleArea():
    def test_triangle_area1(self):
        assert physics.triangle_area(1, 1, 0) == 0

    def test_triangle_area2(self):
        assert physics.triangle_area(3, 4, 5) == 0.5 * 3 * 4


class TestRotationMatrix():
    def test_rotation_matrix1(self):
        for x, y, z in itertools.product(np.linspace(-1, 1, 5), repeat=3):
            if x != 0 or y != 0 or z != 0:
                assert np.all(physics.rotation_matrix(
                    np.array([x, y, z]), 0) == np.identity(3))

    def test_rotation_matrix2(self):
        for x, y, z in itertools.product(np.linspace(-1, 1, 5), repeat=3):
            if x != 0 or y != 0 or z != 0:
                assert np.all(np.round(physics.rotation_matrix(
                    np.array([x, y, z]), 2 * np.pi), 10) == np.identity(3))

    # noinspection PyTypeChecker
    def test_rotation_matrix3(self):
        for angle in np.linspace(-np.pi * 2, np.pi * 2, 100):
            assert np.all(np.round(physics.rotation_matrix(np.array([0, 0, 1]), angle), 10) == np.round(np.array(
                [
                    [math.cos(angle), -math.sin(angle), 0],
                    [math.sin(angle), math.cos(angle), 0],
                    [0, 0, 1]
                ]), 10))


table_side_1 = table_sprites.TableSide([[0, 0], [10, 10]])
table_side_2 = table_sprites.TableSide([[0, 0], [10, 0]])
ball1 = ball.Ball()
ball2 = ball.Ball()

ball1.move_to((0, 0))
ball1.set_velocity((1, 1))

fortyfive_degree_position = np.array(
    [np.sin(np.pi / 4), np.cos(np.pi / 4)]) * ball_radius * 2


class TestBall():
    # distance tests will check if the ball distance function is working
    # properly

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

    # reflection line tests
    # the lines should only reflect balls coming from one direction so the
    # balls wouldn't get stuck in the reflection lines
    def test_line_ball_collision_check1(self):
        ball1.move_to(table_side_1.middle +
                      np.array([1., -1.]) * (ball_radius ** 0.5))
        ball1.set_velocity([1, -1])
        assert physics.line_ball_collision_check(table_side_1, ball1)

    def test_line_ball_collision_check2(self):
        ball1.move_to(table_side_1.middle +
                      np.array([1., -1.]) * (ball_radius ** 0.5))
        ball1.set_velocity([-1, 1])
        assert not physics.line_ball_collision_check(table_side_1, ball1)

    def test_line_ball_collision_check3(self):
        ball1.move_to(table_side_1.middle + 1)
        ball1.set_velocity([1, -1])
        assert physics.line_ball_collision_check(table_side_1, ball1)

    def test_line_ball_collision_check4(self):
        ball1.move_to(table_side_1.middle + ball_radius)
        ball1.set_velocity([-1, 1])
        assert not physics.line_ball_collision_check(table_side_1, ball1)

    def test_line_ball_collision5(self):
        ball1.move_to([5, ball_radius])
        ball1.set_velocity([1, -1])
        assert physics.line_ball_collision_check(table_side_2, ball1)
        physics.collide_line_ball(table_side_2, ball1)
        assert np.all(np.around(ball1.velocity, 0) == [1., 1.])

    def test_line_ball_collision6(self):
        ball1.move_to(table_side_1.middle +
                      np.array([1., -1.]) * (ball_radius ** 0.5))
        ball1.set_velocity([1, -1])
        assert physics.line_ball_collision_check(table_side_1, ball1)
        physics.collide_line_ball(table_side_1, ball1)
        assert np.all(np.around(ball1.velocity, 0) == [-1., 1.])

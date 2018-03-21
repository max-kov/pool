import numpy as np

from pool import ball
from pool import physics
from pool import table_sprites
from pool.config import ball_radius

table_side_1 = table_sprites.TableSide([[0, 0], [10, 10]])
table_side_2 = table_sprites.TableSide([[0, 0], [10, 0]])
ball1 = ball.Ball()

ball1.move_to((0, 0))
ball1.set_velocity((1, 1))


class TestBallLineCollision():
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

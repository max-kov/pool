import numpy as np

from pool import physics


class TestPointDistance():
    def test_point_distance1(self):
        assert physics.point_distance(np.array([0, 0]), np.array([3, 4])) == 5

    def test_point_distance2(self):
        assert physics.point_distance(
            np.array([0, -10]), np.array([0, -10])) == 0

    def test_point_distance3(self):
        assert physics.point_distance(
            np.array([10, 0]), np.array([-10, 0])) == 20

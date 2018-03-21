import itertools

import numpy as np

from pool import physics

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

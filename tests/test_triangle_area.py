from pool import physics

class TestTriangleArea():
    def test_triangle_area1(self):
        assert physics.triangle_area(1, 1, 0) == 0

    def test_triangle_area2(self):
        assert physics.triangle_area(3, 4, 5) == 0.5 * 3 * 4

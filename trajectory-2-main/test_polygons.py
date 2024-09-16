import polygons as pg


def test_on_segment():
    assert pg.on_segment((1, 5), (2, 5), (3, 5))
    assert not pg.on_segment((1, 1), (3, 3), (2, 2))
    assert pg.on_segment((1, 5), (1, 5), (3, 5))


def test_orientation():
    assert pg.orientation((0, 0), (0, 1), (2, 1)) == "clockwise"
    assert pg.orientation((0, 0), (2, 1), (0, 1)) == "counterclockwise"
    assert pg.orientation((0, 0), (0, 1), (0, 3)) == "collinear"
    assert pg.orientation((2, 2), (2, 2), (2, 2)) == "collinear"


def test_intersection_segments():
    assert pg.intersection_segments((0, 0), (3, 0), (1, -1), (1, 1))
    assert pg.intersection_segments((0, 0), (3, 0), (3, 0), (5, 0))
    assert pg.intersection_segments((0, 0), (3, 0), (2, 0), (5, 0))
    assert not pg.intersection_segments((0, 0), (3, 0), (4, 0), (5, 0))
    assert not pg.intersection_segments((0, 0), (3, 0), (0, 2), (5, 2))


def test_polygons_and_segment():
    polygon = [
        {
            "id": 3001,
            "x": 0.000000,
            "y": 0.000000
        },
        {
            "id": 3002,
            "x": 0.000000,
            "y": 1.000000
        },
        {
            "id": 3003,
            "x": 1.000000,
            "y": 1.000000
        },
        {
            "id": 3004,
            "x": 1.000000,
            "y": 0.000000
        },
    ]
    assert pg.polygons_and_segment(polygon, (0, 0.5), (2, 0.5))
    assert pg.polygons_and_segment(polygon, (0, 0), (0, 1))


def test_vector():
    assert pg.vector((0, 1), (2, 2)) == (2, 1)


def test_normal_vector():
    assert pg.normal_vector((-1, 1)) == (1, 1)
    assert pg.normal_vector((0, 1)) == (1, 0)


def test_length_vector():
    assert pg.length_vector((1, 1)) == 2 ** 0.5


def test_orientation_vectors():
    assert not pg.orientation_vectors((0, 3), (-2, 1), (2, 1))
    assert pg.orientation_vectors((0, 3), (0, 1), (2, 1))
    assert pg.orientation_vectors((0, 3), (3, 2), (2, 1))


def test_tangent():
    polygon = [
        {
            "id": 3001,
            "x": 4.000000,
            "y": 4.000000
        },
        {
            "id": 3002,
            "x": 4.000000,
            "y": 8.000000
        },
        {
            "id": 3003,
            "x": 8.000000,
            "y": 8.000000
        },
        {
            "id": 3004,
            "x": 8.000000,
            "y": 4.000000
        }
    ]
    point1 = (4, 3)
    point2 = (6, 10)
    assert pg.tangent(polygon, point1) == (3001, 3002)
    assert pg.tangent(polygon, point2) == (3002, 3003)


def test_length_route():
    route1 = [(0, 0), (1, 0)]
    route2 = [(0, 0), (3, 0), (3, 4)]
    route3 = [(0, 0), (0, 0)]
    assert pg.length_route(route1) == 1
    assert pg.length_route(route2) == 7
    assert pg.length_route(route3) == 0


def test_processing_route():
    polygon = [
        {
            "id": 3001,
            "x": 4.000000,
            "y": 4.000000
        },
        {
            "id": 3002,
            "x": 4.000000,
            "y": 8.000000
        },
        {
            "id": 3003,
            "x": 8.000000,
            "y": 8.000000
        },
        {
            "id": 3004,
            "x": 8.000000,
            "y": 4.000000
        }
    ]
    a = (4, 3)
    b = (8, 9)
    p = 3001
    q = 3003
    assert pg.processing_route(polygon, a, b, p, q) == [a, (4, 4), (4, 4), b]

import forbidden_zone as fz
import numpy as np


def test_circle_and_segment():
    assert fz.circle_and_segment(a_x=1, a_y=1, b_x=7, b_y=7, c_x=4, c_y=4, r=1) == True  # noqa: E712
    assert fz.circle_and_segment(a_x=1, a_y=1, b_x=7, b_y=7, c_x=7, c_y=4, r=1) == False  # noqa: E712


def test_tangent():
    accuracy = 0.000001
    assert np.allclose(fz.tangent(a_x=1, a_y=1, c_x=2, c_y=2, r=1), [(2, 1), (1, 2)],
                       atol=accuracy) == True  # noqa: E712
    assert np.allclose(fz.tangent(a_x=3, a_y=3, c_x=2, c_y=2, r=1), [(2, 3), (3, 2)],
                       atol=accuracy) == True  # noqa: E712


def test_segment_length():
    assert fz.segment_length((0, 0), (5, 0)) == 5
    assert fz.segment_length((2, 3), (7, 1)) == np.sqrt(29)


def test_tetha():
    accuracy = 0.000001
    assert np.allclose(fz.tetha(tuple_1=(5, 0), tuple_2=(0, 5), c_y=0, r=5), 90, atol=accuracy) == True  # noqa: E712
    assert np.allclose(fz.tetha(tuple_1=(5, 0), tuple_2=(-5, 0), c_y=0, r=5), 180, atol=accuracy) == True  # noqa: E712
    assert np.allclose(fz.tetha(tuple_1=(5, 0), tuple_2=(0, -5), c_y=0, r=5), 270, atol=accuracy) == True  # noqa: E712
    assert np.allclose(fz.tetha(tuple_1=(5, 0), tuple_2=(5, 0), c_y=0, r=5), 0, atol=accuracy) == True  # noqa: E712


def test_arc_length():
    accuracy = 0.000001
    assert np.allclose(fz.arc_length(tuple_1=(1, 0), tuple_2=(-1, 0), r=1), np.pi, atol=accuracy) == True  # noqa: E712
    assert np.allclose(fz.arc_length(tuple_1=(np.sqrt(0.5), np.sqrt(0.5)), tuple_2=(np.sqrt(0.5), -np.sqrt(0.5)), r=1),
                       0.5 * np.pi, atol=accuracy) == True  # noqa: E712


def test_processing_route():
    accuracy = 0.000001
    tangents_1 = [(2, 1), (1, 2), (2, 3), (3, 2)]
    tangents_2 = [(2, 1), (1, 2), (1, 2), (2, 3)]
    assert np.allclose(fz.processing_route(tangents=tangents_1, a_x=1, a_y=1, b_x=3, b_y=3, r=1), (1, 2 + 0.5 * np.pi),
                       atol=accuracy) == True  # noqa: E712
    assert np.allclose(fz.processing_route(tangents=tangents_2, a_x=1, a_y=1, b_x=1, b_y=3, r=1), (2, 2),
                       atol=accuracy) == True  # noqa: E712


def test_detour_route():
    tangents_1 = [(2, 1), (1, 2), (2, 3), (3, 2)]
    line_1 = (1, 1) + tangents_1[0]
    line_2 = tangents_1[3] + (3, 3)
    arc = ((2, 2), 1, 1, 270, 360)
    assert fz.detour_route(number_route=1, a_x=1, a_y=1, b_x=3, b_y=3, c_x=2, c_y=2, r=1, tangents=tangents_1) == {
        'line_1': line_1, 'arc': arc, 'line_2': line_2}


def test_forbidden_zone():
    data_points = [{'id': 1, 'x': 1.0, 'y': 1.0}, {'id': 2, 'x': 3.0, 'y': 3.0}]
    data_pvo = [{'id': 1, 'x': 2.0, 'y': 2.0, 'r': 1000}]
    matrix = [[np.inf, 1., 2.],
              [1., np.inf, 2.82842712],
              [2., 2.82842712, np.inf]]
    tangents_1 = [(2, 1), (1, 2), (2, 3), (3, 2)]
    line_1 = (1, 1) + tangents_1[0]
    line_2 = tangents_1[3] + (3, 3)
    arc = ((2, 2), 1, 1, 270, 360)
    assert fz.forbidden_zone(data_points, data_pvo, matrix) == {
        (1, 2): {'line_1': line_1, 'arc': arc, 'line_2': line_2}}

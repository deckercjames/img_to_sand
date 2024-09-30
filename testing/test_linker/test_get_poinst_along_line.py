

from src.linker.linker import get_all_points_along_line



def test_get_line_points_basic():
    test_p0 = (1,1)
    test_p1 = (3,3)
    expected_points = [(1,1), (2,2), (3,3)]
    recv_points = get_all_points_along_line(test_p0, test_p1)
    assert recv_points == expected_points


def test_get_line_points_negative_slope():
    test_p0 = (3,1)
    test_p1 = (1,3)
    expected_points = [(3,1), (2,2), (1,3)]
    recv_points = get_all_points_along_line(test_p0, test_p1)
    assert recv_points == expected_points


def test_get_line_points_shallow_angle():
    test_p0 = (1,1)
    test_p1 = (4,7)
    expected_points = [(1,1), (2,2), (2,3), (3,4), (3,5), (4,6), (4,7)]
    recv_points = get_all_points_along_line(test_p0, test_p1)
    assert recv_points == expected_points


def test_get_line_points_hor():
    test_p0 = (1,1)
    test_p1 = (1,3)
    expected_points = [(1,1), (1,2), (1,3)]
    recv_points = get_all_points_along_line(test_p0, test_p1)
    assert recv_points == expected_points


def test_get_line_points_vert():
    test_p0 = (1,1)
    test_p1 = (3,1)
    expected_points = [(1,1), (2,1), (3,1)]
    recv_points = get_all_points_along_line(test_p0, test_p1)
    assert recv_points == expected_points


def test_get_line_points_same():
    test_p0 = (1,1)
    test_p1 = (1,1)
    expected_points = [(1,1)]
    recv_points = get_all_points_along_line(test_p0, test_p1)
    assert recv_points == expected_points


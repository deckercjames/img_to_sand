
from process_image import get_all_mask_contours
from copy import deepcopy


def test_get_grid_mask_contours_basic():
    test_grid_mask = [
        [False, False, False, False, False],
        [False, False, True,  True,  False],
        [False, False, False, False, False],
    ]
    test_grid_mask_unchanged = deepcopy(test_grid_mask)
    expected_result = [
        [(1,2), (1,3), (1,4), (2,4), (2,3), (2,2)],
    ]
    recv_contours = get_all_mask_contours(test_grid_mask)
    assert recv_contours == expected_result
    assert test_grid_mask == test_grid_mask_unchanged


def test_get_grid_mask_contours_two():
    test_grid_mask = [
        [False, False, True ],
        [True,  True,  False],
    ]
    test_grid_mask_unchanged = deepcopy(test_grid_mask)
    expected_result = [
        [(0,2), (0,3), (1,3), (1,2)],
        [(1,0), (1,1), (1,2), (2,2), (2,1), (2,0)],
    ]
    recv_contours = get_all_mask_contours(test_grid_mask)
    assert recv_contours == expected_result
    assert test_grid_mask == test_grid_mask_unchanged



from process_image import get_total_blob_mask
from copy import deepcopy


def test_get_total_blob_mask_one_square():
    test_contour = [(0, 0), (0, 1), (1, 1), (1, 0)]
    test_contour_unchanged = deepcopy(test_contour)
    recv_total_blob_mask = get_total_blob_mask(test_contour, 1, 1)
    expected_total_blob_mask = [
        [True]
    ]
    assert recv_total_blob_mask == expected_total_blob_mask
    assert test_contour == test_contour_unchanged


def test_get_total_blob_mask_basic():
    test_contour = [(1, 2), (1, 3), (1, 4), (2, 4), (2, 3), (2, 2)]
    test_contour_unchanged = deepcopy(test_contour)
    recv_total_blob_mask = get_total_blob_mask(test_contour, 3, 5)
    expected_total_blob_mask = [
        [False, False, False, False, False],
        [False, False, True,  True,  False],
        [False, False, False, False, False],
    ]
    assert recv_total_blob_mask == expected_total_blob_mask
    assert test_contour == test_contour_unchanged


def test_get_total_blob_mask_with_inner_area():
    test_contour = [(1,1), (1,2), (1,3), (1,4), (2,4), (3,4), (4,4), (4,3), (4,2), (4,1), (3,1), (2,1)]
    test_contour_unchanged = deepcopy(test_contour)
    recv_total_blob_mask = get_total_blob_mask(test_contour, 5, 5)
    expected_total_blob_mask = [
        [False, False, False, False, False],
        [False, True,  True,  True,  False],
        [False, True,  True,  True,  False],
        [False, True,  True,  True,  False],
        [False, False, False, False, False],
    ]
    assert recv_total_blob_mask == expected_total_blob_mask
    assert test_contour == test_contour_unchanged


def test_get_total_blob_mask_with_concavity():
    test_contour = [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (2,2), (1,2), (1,1), (2,1), (2,2), (3,2), (4,2), (4,1), (4,0), (3,0), (2,0), (1,0)]
    test_contour_unchanged = deepcopy(test_contour)
    recv_total_blob_mask = get_total_blob_mask(test_contour, 4, 3)
    expected_total_blob_mask = [
        [True, True,  True ],
        [True, False, True ],
        [True, True,  False],
        [True, True,  False],
    ]
    assert recv_total_blob_mask == expected_total_blob_mask
    assert test_contour == test_contour_unchanged
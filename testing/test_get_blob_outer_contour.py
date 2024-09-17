
from process_image import get_blob_outer_contour
from copy import deepcopy


def test_basic_get_blob_outer_contour():
    test_blob_mask = [
        [False, False, False, False, False],
        [False, False, True,  True,  False],
        [False, False, False, False, False],
    ]
    test_blob_mask_exp_unchanged = deepcopy(test_blob_mask)
    recv_blob_contour = get_blob_outer_contour(test_blob_mask, 1, 2)
    assert type(recv_blob_contour) == list
    expected_result = [(1, 2), (1, 3), (1, 4), (2, 4), (2, 3), (2, 2)]
    assert recv_blob_contour == expected_result
    assert test_blob_mask == test_blob_mask_exp_unchanged
    pass


def test_get_blob_outer_contour_all_angles():
    test_blob_mask = [
        [False, False, False, False, False, False],
        [False, False, False, True,  False, False],
        [False, True,  True,  True,  True,  False],
        [False, True,  True,  True,  True,  False],
        [False, False, False, True,  False, False],
        [False, False, False, False, False, False],
    ]
    test_blob_mask_exp_unchanged = deepcopy(test_blob_mask)
    recv_blob_contour = get_blob_outer_contour(test_blob_mask, 1, 3)
    assert type(recv_blob_contour) == list
    expected_result = [(1, 3), (1, 4), (2, 4), (2, 5), (3, 5), (4, 5), (4, 4), (5, 4), (5, 3), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1), (2, 2), (2, 3)]
    assert recv_blob_contour == expected_result
    assert test_blob_mask == test_blob_mask_exp_unchanged


def test_get_blob_outer_contour_touching_edges():
    test_blob_mask = [
        [1],
    ]
    test_blob_mask_exp_unchanged = deepcopy(test_blob_mask)
    recv_blob_contour = get_blob_outer_contour(test_blob_mask, 0, 0)
    assert type(recv_blob_contour) == list
    expected_result = [(0, 0), (0, 1), (1, 1), (1, 0)]
    assert recv_blob_contour == expected_result
    assert test_blob_mask == test_blob_mask_exp_unchanged

    
def test_get_blob_outer_contour_with_concavity():
    test_blob_mask = [
        [True, True,  True ],
        [True, False, True ],
        [True, True,  False],
    ]
    test_blob_mask_exp_unchanged = deepcopy(test_blob_mask)
    recv_blob_contour = get_blob_outer_contour(test_blob_mask, 0, 0)
    assert type(recv_blob_contour) == list
    expected_result = [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (2,2), (1,2), (1,1), (2,1), (2,2), (3,2), (3,1), (3,0), (2,0), (1,0)]
    assert recv_blob_contour == expected_result
    assert test_blob_mask == test_blob_mask_exp_unchanged

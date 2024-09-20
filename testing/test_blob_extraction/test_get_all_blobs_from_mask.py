
from src.topography import get_all_blobs_from_mask
from src.blob_extraction import Blob
from copy import deepcopy


def test_get_grid_mask_contours_basic():
    test_grid_mask = [
        [False, False, False, False, False],
        [False, False, True,  True,  False],
        [False, False, False, False, False],
    ]
    test_grid_mask_unchanged = deepcopy(test_grid_mask)
    expected_result = [
        Blob(
            # Outer contour
            [(1,2), (1,3), (1,4), (2,4), (2,3), (2,2)],
            # Blob mask
            [
                [False, False, False, False, False],
                [False, False, True,  True,  False],
                [False, False, False, False, False],
            ],
            # Total mask
            [
                [False, False, False, False, False],
                [False, False, True,  True,  False],
                [False, False, False, False, False],
            ],
        )
    ]
    recv_contours = get_all_blobs_from_mask(test_grid_mask)
    assert recv_contours == expected_result
    assert test_grid_mask == test_grid_mask_unchanged


def test_get_grid_mask_contours_two():
    test_grid_mask = [
        [False, False, True ],
        [True,  True,  False],
    ]
    test_grid_mask_unchanged = deepcopy(test_grid_mask)
    expected_result = [
        Blob(
            # Outer contour
            [(0,2), (0,3), (1,3), (1,2)],
            # Blob mask
            [
                [False, False, True ],
                [False, False, False],
            ],
            # Total mask
            [
                [False, False, True ],
                [False, False, False],
            ],
        ),
        Blob(
            # Outer contour
            [(1,0), (1,1), (1,2), (2,2), (2,1), (2,0)],
            # Blob mask
            [
                [False, False, False],
                [True,  True,  False],
            ],
            # Total mask
            [
                [False, False, False],
                [True,  True,  False],
            ],
        )
    ]
    recv_contours = get_all_blobs_from_mask(test_grid_mask)
    assert recv_contours == expected_result
    assert test_grid_mask == test_grid_mask_unchanged


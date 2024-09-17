
from process_image import get_flood_fill_blob_mask
from copy import deepcopy

def test_pixel_flood_fill_basic():
    test_pixel_grid = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]
    test_blob_mask_exp_unchanged = deepcopy(test_pixel_grid)
    recieved_blob_mask = get_flood_fill_blob_mask(test_pixel_grid, 1, 1)
    exp_blob_mask = [
        [False, False, False, False],
        [False, True,  True,  False],
        [False, False, False, False],
    ]
    assert recieved_blob_mask == exp_blob_mask
    assert test_pixel_grid == test_blob_mask_exp_unchanged


def test_pixel_flood_fill_to_bounds():
    """
    The function should be able to fill up to the edge
    """
    test_pixel_grid = [
        [0, 0, 1, 1],
        [0, 1, 1, 1],
        [1, 1, 0, 0],
    ]
    test_blob_mask_exp_unchanged = deepcopy(test_pixel_grid)
    recieved_blob_mask = get_flood_fill_blob_mask(test_pixel_grid, 1, 1)
    exp_blob_mask = [
        [False, False, True,  True ],
        [False, True,  True,  True ],
        [True,  True,  False, False],
    ]
    assert recieved_blob_mask == exp_blob_mask
    assert test_pixel_grid == test_blob_mask_exp_unchanged


def test_pixel_flood_fill_no_diag():
    """
    The flood fill shoudl not jump diagonals
    """
    test_pixel_grid = [
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [1, 0, 0, 1],
    ]
    test_blob_mask_exp_unchanged = deepcopy(test_pixel_grid)
    recieved_blob_mask = get_flood_fill_blob_mask(test_pixel_grid, 1, 1)
    exp_blob_mask = [
        [False, False, False, False],
        [False, True,  True,  False],
        [False, False, False, False],
    ]
    assert recieved_blob_mask == exp_blob_mask
    assert test_pixel_grid == test_blob_mask_exp_unchanged


def test_pixel_flood_fill_differnt_val_neighbor():
    """
    The flood fill shoudl not jump diagonals
    """
    test_pixel_grid = [
        [0, 2, 3, 1],
        [0, 1, 1, 2],
        [5, 5, 5, 1],
    ]
    test_blob_mask_exp_unchanged = deepcopy(test_pixel_grid)
    recieved_blob_mask = get_flood_fill_blob_mask(test_pixel_grid, 1, 1)
    exp_blob_mask = [
        [False, False, False, False],
        [False, True,  True,  False],
        [False, False, False, False],
    ]
    assert recieved_blob_mask == exp_blob_mask
    assert test_pixel_grid == test_blob_mask_exp_unchanged


def test_pixel_flood_fill_with_void_basic():
    test_pixel_grid = [
        [0, 0, 0, 0],
        [0, 1, 1, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 1],
    ]
    test_blob_mask_exp_unchanged = deepcopy(test_pixel_grid)
    recieved_blob_mask = get_flood_fill_blob_mask(test_pixel_grid, 1, 1)
    exp_blob_mask = [
        [False, False, False, False],
        [False, True,  True,  True ],
        [False, True,  False, True ],
        [False, True,  True,  True ],
    ]
    assert recieved_blob_mask == exp_blob_mask
    assert test_pixel_grid == test_blob_mask_exp_unchanged

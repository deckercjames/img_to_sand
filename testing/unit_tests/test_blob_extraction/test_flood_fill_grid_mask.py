
from src.linker.linkable_entity.topography import get_flood_fill_grid_mask
import numpy as np

def test_grid_mask_flood_fill_basic():
    test_pixel_grid = np.array([
        [False, False, False, False],
        [False, True,  True,  False],
        [False, False, False, False],
    ])
    test_blob_mask_exp_unchanged = test_pixel_grid.copy()
    recieved_blob_mask = get_flood_fill_grid_mask(test_pixel_grid, 1, 1)
    exp_blob_mask = np.array([
        [False, False, False, False],
        [False, True,  True,  False],
        [False, False, False, False],
    ])
    assert (recieved_blob_mask == exp_blob_mask).all()
    assert (test_pixel_grid == test_blob_mask_exp_unchanged).all()


def test_grid_mask_flood_fill_to_bounds():
    """
    The function should be able to fill up to the edge
    """
    test_pixel_grid = np.array([
        [False, False, True,  True ],
        [False, True,  True,  True ],
        [True,  True,  False, False],
    ])
    test_blob_mask_exp_unchanged = test_pixel_grid.copy()
    recieved_blob_mask = get_flood_fill_grid_mask(test_pixel_grid, 1, 1)
    exp_blob_mask = np.array([
        [False, False, True,  True ],
        [False, True,  True,  True ],
        [True,  True,  False, False],
    ])
    assert (recieved_blob_mask == exp_blob_mask).all()
    assert (test_pixel_grid == test_blob_mask_exp_unchanged).all()


def test_grid_mask_flood_fill_no_diag():
    """
    The flood fill shoudl not jump diagonals
    """
    test_pixel_grid = np.array([
        [True,  False, False, True] ,
        [False, True,  True,  False],
        [True,  False, False, True] ,
    ])
    test_blob_mask_exp_unchanged = test_pixel_grid.copy()
    recieved_blob_mask = get_flood_fill_grid_mask(test_pixel_grid, 1, 1)
    exp_blob_mask = np.array([
        [False, False, False, False],
        [False, True,  True,  False],
        [False, False, False, False],
    ])
    assert (recieved_blob_mask == exp_blob_mask).all()
    assert (test_pixel_grid == test_blob_mask_exp_unchanged).all()


def test_grid_mask_flood_fill_with_void_basic():
    test_pixel_grid = np.array([
        [False, False, False, False],
        [False, True,  True,  True ],
        [False, True,  False, True ],
        [False, True,  True,  True ],
    ])
    test_blob_mask_exp_unchanged = test_pixel_grid.copy()
    recieved_blob_mask = get_flood_fill_grid_mask(test_pixel_grid, 1, 1)
    exp_blob_mask = np.array([
        [False, False, False, False],
        [False, True,  True,  True ],
        [False, True,  False, True ],
        [False, True,  True,  True ],
    ])
    assert (recieved_blob_mask == exp_blob_mask).all()
    assert (test_pixel_grid == test_blob_mask_exp_unchanged).all()

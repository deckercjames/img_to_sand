

from src.utils import get_numpy_mask_with_inward_bleed
from copy import deepcopy
import numpy as np

def test_inward_bleed_single_square():
    test_grid_mask = np.array([
        [False, False, False],
        [False, True,  False],
        [False, False, False],
    ])
    test_grid_mask_unchanged = test_grid_mask.copy()
    recv_grid_mask = get_numpy_mask_with_inward_bleed(test_grid_mask)
    exp_grid_mask = np.array([
        [False, False, False],
        [False, False, False],
        [False, False, False],
    ])
    assert (recv_grid_mask == exp_grid_mask).all()
    assert (test_grid_mask == test_grid_mask_unchanged).all()


def test_inward_bleed_3x3():
    test_grid_mask = np.array([
        [False, False, False, False, False],
        [False, True,  True,  True,  False],
        [False, True,  True,  True,  False],
        [False, True,  True,  True,  False],
        [False, False, False, False, False],
    ])
    test_grid_mask_unchanged = test_grid_mask.copy()
    recv_grid_mask = get_numpy_mask_with_inward_bleed(test_grid_mask)
    exp_grid_mask = np.array([
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, True,  False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
    ])
    assert (recv_grid_mask == exp_grid_mask).all()
    assert (test_grid_mask == test_grid_mask_unchanged).all()


def test_inward_bleed_3x3_at_bounds():
    test_grid_mask = np.array([
        [True,  True,  True ],
        [True,  True,  True ],
        [True,  True,  True ],
    ])
    test_grid_mask_unchanged = test_grid_mask.copy()
    recv_grid_mask = get_numpy_mask_with_inward_bleed(test_grid_mask)
    exp_grid_mask = np.array([
        [False, False, False],
        [False, True,  False],
        [False, False, False],
    ])
    assert (recv_grid_mask == exp_grid_mask).all()
    assert (test_grid_mask == test_grid_mask_unchanged).all()


def test_inward_bleed_5x5_triangle():
    test_grid_mask = np.array([
        [False, False, False, False, True ],
        [False, False, False, True,  True ],
        [False, False, True,  True,  True ],
        [False, True,  True,  True,  True ],
        [True,  True,  True,  True,  True ],
    ])
    test_grid_mask_unchanged = test_grid_mask.copy()
    recv_grid_mask = get_numpy_mask_with_inward_bleed(test_grid_mask)
    exp_grid_mask = np.array([
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, True,  False],
        [False, False, True,  True,  False],
        [False, False, False, False, False],
    ])
    assert (recv_grid_mask == exp_grid_mask).all()
    assert (test_grid_mask == test_grid_mask_unchanged).all()



def test_inward_bleed_5x5_triangle_diag_true():
    test_grid_mask = np.array([
        [False, False, False, False, True ],
        [False, False, False, True,  True ],
        [False, False, True,  True,  True ],
        [False, True,  True,  True,  True ],
        [True,  True,  True,  True,  True ],
    ])
    test_grid_mask_unchanged = test_grid_mask.copy()
    recv_grid_mask = get_numpy_mask_with_inward_bleed(test_grid_mask, diag_bleed=True)
    exp_grid_mask = np.array([
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, True,  False],
        [False, False, False, False, False],
    ])
    assert (recv_grid_mask == exp_grid_mask).all()
    assert (test_grid_mask == test_grid_mask_unchanged).all()


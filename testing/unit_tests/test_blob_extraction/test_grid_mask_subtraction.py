
from src.utils import get_numpy_grid_mask_subtraction
from copy import deepcopy
import numpy as np

def test_get_grid_mask_subtraction_basic():
    minuend = np.array([
        [True, False],
        [True, False],
    ])
    subtrahend = np.array([
        [True,  True ],
        [False, False],
    ])
    exp_result = np.array([
        [False, False],
        [True,  False],
    ])
    exp_minuend_unchanged = deepcopy(minuend)
    exp_subtrahend_unchanged = deepcopy(subtrahend)
    result = get_numpy_grid_mask_subtraction(minuend, subtrahend)
    assert (result == exp_result).all
    assert (minuend == exp_minuend_unchanged).all
    assert (subtrahend == exp_subtrahend_unchanged).all
    
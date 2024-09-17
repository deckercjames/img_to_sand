
from process_image import grid_mask_subtraction
from copy import deepcopy


def test_grid_mask_subtraction_basic():
    minuend = [
        [True, False],
        [True, False],
    ]
    subtrahend = [
        [True,  True ],
        [False, False],
    ]
    exp_result = [
        [False, False],
        [True,  False],
    ]
    exp_minuend_unchanged = deepcopy(minuend)
    exp_subtrahend_unchanged = deepcopy(subtrahend)
    result = grid_mask_subtraction(minuend, subtrahend)
    assert result == exp_result
    assert minuend == exp_minuend_unchanged
    assert subtrahend == exp_subtrahend_unchanged
    


from src.linker.linkable_entity.topography import get_mask_with_inward_bleed
from copy import deepcopy


def test_inward_bleed_single_square():
    test_grid_mask = [
        [False, False, False],
        [False, True,  False],
        [False, False, False],
    ]
    test_grid_mask_unchanged = deepcopy(test_grid_mask)
    recv_grid_mask = get_mask_with_inward_bleed(test_grid_mask)
    exp_grid_mask = [
        [False, False, False],
        [False, False, False],
        [False, False, False],
    ]
    assert recv_grid_mask == exp_grid_mask
    assert test_grid_mask == test_grid_mask_unchanged


def test_inward_bleed_3x3():
    test_grid_mask = [
        [False, False, False, False, False],
        [False, True,  True,  True,  False],
        [False, True,  True,  True,  False],
        [False, True,  True,  True,  False],
        [False, False, False, False, False],
    ]
    test_grid_mask_unchanged = deepcopy(test_grid_mask)
    recv_grid_mask = get_mask_with_inward_bleed(test_grid_mask)
    exp_grid_mask = [
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, True,  False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
    ]
    assert recv_grid_mask == exp_grid_mask
    assert test_grid_mask == test_grid_mask_unchanged


def test_inward_bleed_3x3_at_bounds():
    test_grid_mask = [
        [True,  True,  True ],
        [True,  True,  True ],
        [True,  True,  True ],
    ]
    test_grid_mask_unchanged = deepcopy(test_grid_mask)
    recv_grid_mask = get_mask_with_inward_bleed(test_grid_mask)
    exp_grid_mask = [
        [False, False, False],
        [False, True,  False],
        [False, False, False],
    ]
    assert recv_grid_mask == exp_grid_mask
    assert test_grid_mask == test_grid_mask_unchanged


def test_inward_bleed_5x5_triangle():
    test_grid_mask = [
        [False, False, False, False, True ],
        [False, False, False, True,  True ],
        [False, False, True,  True,  True ],
        [False, True,  True,  True,  True ],
        [True,  True,  True,  True,  True ],
    ]
    test_grid_mask_unchanged = deepcopy(test_grid_mask)
    recv_grid_mask = get_mask_with_inward_bleed(test_grid_mask)
    exp_grid_mask = [
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, True,  False],
        [False, False, True,  True,  False],
        [False, False, False, False, False],
    ]
    assert recv_grid_mask == exp_grid_mask
    assert test_grid_mask == test_grid_mask_unchanged



def test_inward_bleed_5x5_triangle_diag_true():
    test_grid_mask = [
        [False, False, False, False, True ],
        [False, False, False, True,  True ],
        [False, False, True,  True,  True ],
        [False, True,  True,  True,  True ],
        [True,  True,  True,  True,  True ],
    ]
    test_grid_mask_unchanged = deepcopy(test_grid_mask)
    recv_grid_mask = get_mask_with_inward_bleed(test_grid_mask, diag_bleed=True)
    exp_grid_mask = [
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, True,  False],
        [False, False, False, False, False],
    ]
    assert recv_grid_mask == exp_grid_mask
    assert test_grid_mask == test_grid_mask_unchanged


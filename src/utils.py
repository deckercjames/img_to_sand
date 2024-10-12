
from copy import deepcopy
from typing import List


def get_list_element_cyclic(list, i):
    return list[i % len(list)]


def get_neighbor_points(r: int, c: int) -> List[tuple[int, int]]:
    return [
        (r-1, c  ),
        (r-1, c+1),
        (r,   c+1),
        (r+1, c+1),
        (r+1, c  ),
        (r+1, c-1),
        (r,   c-1),
        (r-1, c-1),
    ]


def check_grid_element_safe(grid, r, c, default=None):
    if r < 0 or r >= len(grid):
        return default
    if c < 0 or c >= len(grid[r]):
        return default
    return grid[r][c]


def get_grid_mask_subtraction(grid_mask, grid_mask_subtrahend):
    if len(grid_mask) != len(grid_mask_subtrahend) or len(grid_mask[0]) != len(grid_mask_subtrahend[0]):
        raise Exception("Can not subtract different sized masks. ({}x{}) - ({}x{})".format(len(grid_mask), len(grid_mask[0]), len(grid_mask_subtrahend), len(grid_mask_subtrahend[0])))

    return [[(grid_mask[r][c] and not grid_mask_subtrahend[r][c]) for c in range(len(grid_mask[r]))] for r in range(len(grid_mask))]


def get_all_false_mask(num_rows, num_cols):
    return [[False for _ in range(num_cols)] for _ in range(num_rows)]


def get_grid_mask_union(m1, m2):
    if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
        raise Exception("Can not union different sized masks. ({}x{}) U ({}x{})".format(len(m1), len(m1[0]), len(m2), len(m2[0])))

    return [[(m1[r][c] or m2[r][c]) for c in range(len(m1[r]))] for r in range(len(m1))]


def grid_mask_to_str(grid_mask):
    buf = ""
    buf += "+" + "-" * len(grid_mask[0]) + "+\n"
    for row in grid_mask:
        buf += "|"
        for cell in row:
            buf += "#" if cell else " "
        buf += "|\n"
    buf += "+" + "-" * len(grid_mask[0]) + "+\n"
    return buf


def check_mask_intersection(m1, m2):
    if len(m1) != len(m2):
        raise Exception("Can not subtract different sized masks")
    if len(m1[0]) != len(m2[0]):
        raise Exception("Can not subtract different sized masks")
    
    for r in range(len(m1)):
        for c in range(len(m1[0])):
            if m1[r][c] and m2[r][c]:
                return True
    return False
    


def get_mask_with_inward_bleed(grid_mask, diag_bleed=False):
    result = deepcopy(grid_mask)
    
    for r, row in enumerate(grid_mask):
        for c in range(len(row)):
            if r == 0 or r == len(grid_mask) - 1 or c == 0 or c == len(row) - 1:
                result[r][c] = False
                continue
            if not grid_mask[r-1][c] or not grid_mask[r+1][c] or not grid_mask[r][c-1] or not grid_mask[r][c+1]:
                result[r][c] = False
                continue
            if diag_bleed and (not grid_mask[r-1][c+1] or not grid_mask[r+1][c+1] or not grid_mask[r+1][c-1] or not grid_mask[r-1][c-1]):
                result[r][c] = False
                continue
            
    return result

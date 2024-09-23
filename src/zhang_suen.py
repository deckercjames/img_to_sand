
from copy import deepcopy
from src.utils import check_grid_element_safe

def _get_neighbours(image, r, c):
    '''Return 8-neighbours of point p1 of picture, in order'''
    return [
        check_grid_element_safe(image, r-1, c,   default=False),
        check_grid_element_safe(image, r-1, c+1, default=False),
        check_grid_element_safe(image, r,   c+1, default=False),
        check_grid_element_safe(image, r+1, c+1, default=False),
        check_grid_element_safe(image, r+1, c,   default=False),
        check_grid_element_safe(image, r+1, c-1, default=False),
        check_grid_element_safe(image, r,   c-1, default=False),
        check_grid_element_safe(image, r-1, c-1, default=False),
    ]

def _get_transition_count(neighbours):
    n = neighbours + neighbours[0:1]    # P2, ... P9, P2
    return sum((n1, n2) == (False, True) for n1, n2 in zip(n, n[1:]))


def _zhang_suen_errosion_single_step(image, neighbor_indicies_set_1, neighbor_indicies_set_2):
    # Step 1
    changing = []
    for r in range(len(image)):
        for c in range(len(image[r])):
            neighbours = _get_neighbours(image, r, c)
            if (image[r][c] and
                    (any([not neighbours[i-2] for i in neighbor_indicies_set_1])) and   # Neighbors are indexed starting with P2
                    (any([not neighbours[i-2] for i in neighbor_indicies_set_2])) and
                    _get_transition_count(neighbours) == 1 and
                    2 <= sum([1 if n else 0 for n in neighbours]) <= 6):
                changing.append((r,c))
    for r, c in changing:
        image[r][c] = False
    return len(changing)


def zhang_suen_errosion_itteration(image):
    changed_step_1 = _zhang_suen_errosion_single_step(image, (4,6,8), (2,4,6))
    changed_step_2 = _zhang_suen_errosion_single_step(image, (2,6,8), (2,4,8))
    return changed_step_1 or changed_step_2


def zhang_suen_errosion(grid_mask):
    ret_grid_mask = deepcopy(grid_mask)
    while True:
        any_cells_changed = zhang_suen_errosion_itteration(ret_grid_mask)
        if not any_cells_changed:
            break
    return ret_grid_mask

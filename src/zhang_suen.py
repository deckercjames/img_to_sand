
from copy import deepcopy
from src.utils import check_grid_element_safe
from src.utils import grid_mask_subtraction

#==================================================
# Main Zhang Suen Algorithm
#==================================================

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



#==================================================
# Related API Functions
#==================================================

def get_area_blobs(erroded_grid_mask):

    remaining_blobs = [[False for _ in range(len(row))] for row in erroded_grid_mask]

    for r in range(len(erroded_grid_mask) - 1):
        for c in range(len(erroded_grid_mask[r]) - 1):
            if (check_grid_element_safe(erroded_grid_mask, r, c) and
                    check_grid_element_safe(erroded_grid_mask, r, c+1) and
                    check_grid_element_safe(erroded_grid_mask, r+1, c) and
                    check_grid_element_safe(erroded_grid_mask, r+1, c+1)):
                remaining_blobs[r][c] = True
                remaining_blobs[r][c+1] = True
                remaining_blobs[r+1][c] = True
                remaining_blobs[r+1][c+1] = True
    
    return remaining_blobs


def get_flood_fill_area_blobs(original_grid_mask, micro_blob_grid_mask, itterations):
    
    for i in range(itterations):
        intrim_blob_grid_mask = deepcopy(micro_blob_grid_mask)
        for r in range(len(micro_blob_grid_mask)):
            for c in range(len(micro_blob_grid_mask[r])):
                if (not micro_blob_grid_mask[r][c] and
                        original_grid_mask[r][c] and
                        any(_get_neighbours(micro_blob_grid_mask, r, c))):
                    intrim_blob_grid_mask[r][c] = True
        micro_blob_grid_mask = intrim_blob_grid_mask
    return micro_blob_grid_mask


def get_split_lines_and_blobs(blob_grid_mask, itterations):
    
    erroded_grid_mask = deepcopy(blob_grid_mask)
    
    for i in range(itterations):
        zhang_suen_errosion_itteration(erroded_grid_mask)
    
    micro_blob_grid_mask = get_area_blobs(erroded_grid_mask)
    
    blob_only_grid_mask = get_flood_fill_area_blobs(blob_grid_mask, micro_blob_grid_mask, itterations * 2 + 1)
    line_only_grid_mask = grid_mask_subtraction(erroded_grid_mask, blob_only_grid_mask)
    
    return (blob_only_grid_mask, line_only_grid_mask)
    
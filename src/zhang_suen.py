
from copy import deepcopy
from src.utils import check_grid_element_safe

def get_neighbours(image, r, c):
    '''Return 8-neighbours of point p1 of picture, in order'''
    return [
        check_grid_element_safe(image, r-1, c  ),
        check_grid_element_safe(image, r-1, c+1),
        check_grid_element_safe(image, r,   c+1),
        check_grid_element_safe(image, r+1, c+1),
        check_grid_element_safe(image, r+1, c  ),
        check_grid_element_safe(image, r+1, c-1),
        check_grid_element_safe(image, r,   c-1),
        check_grid_element_safe(image, r-1, c-1),
    ]

def get_transition_count(neighbours):
    n = neighbours + neighbours[0:1]    # P2, ... P9, P2
    return sum((n1, n2) == (False, True) for n1, n2 in zip(n, n[1:]))

def zhang_suen_errosion_itteration(image):
    # Step 1
    changing1 = []
    for r in range(len(image)):
        for c in range(len(image[r])):
            P2,P3,P4,P5,P6,P7,P8,P9 = neighbours = get_neighbours(image, r, c)
            if (image[r][c] and    # (Condition 0)
                (not P4 or not P6 or not P8) and   # Condition 4
                (not P2 or not P4 or not P6) and   # Condition 3
                get_transition_count(neighbours) == 1 and # Condition 2
                2 <= sum([1 if n else 0 for n in neighbours]) <= 6):      # Condition 1
                changing1.append((r,c))
    for r, c in changing1:
        image[r][c] = False
    # Step 2
    changing2 = []
    for r in range(len(image)):
        for c in range(len(image[r])):
            P2,P3,P4,P5,P6,P7,P8,P9 = neighbours = get_neighbours(image, r, c)
            if (image[r][c] and    # (Condition 0)
                (not P2 or not P6 or not P8) and   # Condition 4
                (not P2 or not P4 or not P8) and   # Condition 3
                get_transition_count(neighbours) == 1 and # Condition 2
                2 <= sum([1 if n else 0 for n in neighbours]) <= 6):      # Condition 1
                changing2.append((r,c))
    for r, c in changing2:
        image[r][c] = False
    return len(changing1) > 0 or len(changing2) > 0


def zhang_suen_errosion(grid_mask):
    ret_grid_mask = deepcopy(grid_mask)
    while True:
        any_cells_changed = zhang_suen_errosion_itteration(ret_grid_mask)
        if not any_cells_changed:
            break
    return ret_grid_mask

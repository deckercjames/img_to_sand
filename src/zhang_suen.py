
from copy import deepcopy
from src.utils import check_grid_element_safe

def get_neighbours(x, y, image):
    '''Return 8-neighbours of point p1 of picture, in order'''
    i = image
    x1, y1, x_1, y_1 = x+1, y-1, x-1, y+1
    #print ((x,y))
    return [i[y1][x],  i[y1][x1],   i[y][x1],  i[y_1][x1],  # P2,P3,P4,P5
            i[y_1][x], i[y_1][x_1], i[y][x_1], i[y1][x_1]]  # P6,P7,P8,P9

def transitions(neighbours):
    n = neighbours + neighbours[0:1]    # P2, ... P9, P2
    return sum((n1, n2) == (False, True) for n1, n2 in zip(n, n[1:]))

def zhang_suen_errosion_itteration(image):
    # Step 1
    changing1 = []
    for y in range(1, len(image) - 1):
        for x in range(1, len(image[0]) - 1):
            P2,P3,P4,P5,P6,P7,P8,P9 = neighbours = get_neighbours(x, y, image)
            if (image[y][x] and    # (Condition 0)
                (not P4 or not P6 or not P8) and   # Condition 4
                (not P2 or not P4 or not P6) and   # Condition 3
                transitions(neighbours) == 1 and # Condition 2
                2 <= sum([1 if n else 0 for n in neighbours]) <= 6):      # Condition 1
                changing1.append((x,y))
    for x, y in changing1:
        image[y][x] = False
    # Step 2
    changing2 = []
    for y in range(1, len(image) - 1):
        for x in range(1, len(image[0]) - 1):
            P2,P3,P4,P5,P6,P7,P8,P9 = neighbours = get_neighbours(x, y, image)
            if (image[y][x] and    # (Condition 0)
                (not P2 or not P6 or not P8) and   # Condition 4
                (not P2 or not P4 or not P8) and   # Condition 3
                transitions(neighbours) == 1 and # Condition 2
                2 <= sum([1 if n else 0 for n in neighbours]) <= 6):      # Condition 1
                changing2.append((x,y))
    for x, y in changing2:
        image[y][x] = False
    return len(changing1) > 0 or len(changing2) > 0

def zhang_suen_errosion(grid_mask):
    ret_grid_mask = deepcopy(grid_mask)
    while True:
        any_cells_changed = zhang_suen_errosion_itteration(ret_grid_mask)
        if not any_cells_changed:
            break
    return ret_grid_mask

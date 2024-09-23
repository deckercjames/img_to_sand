



def get_list_element_cyclic(list, i):
    return list[i % len(list)]


def check_grid_element_safe(grid, r, c, default=None):
    if r < 0 or r >= len(grid):
        return default
    if c < 0 or c >= len(grid[r]):
        return default
    return grid[r][c]


def grid_mask_subtraction(grid_mask, grid_mask_subtrahend):
    if len(grid_mask) != len(grid_mask_subtrahend):
        raise Exception("Can not subtract different sized masks")
    if len(grid_mask[0]) != len(grid_mask_subtrahend[0]):
        raise Exception("Can not subtract different sized masks")
        
    return [[(grid_mask[r][c] and not grid_mask_subtrahend[r][c]) for c in range(len(grid_mask[r]))] for r in range(len(grid_mask))]


def grid_mask_union(m1, m2):
    if len(m1) != len(m2):
        raise Exception("Can not subtract different sized masks")
    if len(m1[0]) != len(m2[0]):
        raise Exception("Can not subtract different sized masks")
        
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
    
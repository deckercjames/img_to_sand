


def check_grid_element_safe(grid, r, c):
    if r < 0 or r >= len(grid):
        return None
    if c < 0 or c >= len(grid[r]):
        return None
    return grid[r][c]

def grid_mask_subtraction(grid_mask, grid_mask_subtrahend):
    if len(grid_mask) != len(grid_mask_subtrahend):
        raise Exception("Can not subtract different sized masks")
    if len(grid_mask[0]) != len(grid_mask_subtrahend[0]):
        raise Exception("Can not subtract different sized masks")
        
    return [[(grid_mask[r][c] and not grid_mask_subtrahend[r][c]) for c in range(len(grid_mask[r]))] for r in range(len(grid_mask))]


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

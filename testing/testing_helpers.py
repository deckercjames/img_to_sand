



def helper_mask_string_to_bool_mask(str_rep):
    result = []
    for row in str_rep:
        result.append([c == "#" for c in row])
    return result

def helper_grid_mask_to_string(grid_mask):
    buf = ""
    for row in grid_mask:
        for cell in row:
            buf += "#" if cell else " "
        buf += "\n"
    return buf

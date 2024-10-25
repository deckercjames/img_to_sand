
import numpy as np

COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[32m'
COLOR_NONE = '\033[00m'

def helper_mask_string_to_bool_mask(str_rep):
    result = []
    for row in str_rep:
        result_row = []
        for cell in row:
            if cell == "#":
                result_row.append(True)
            elif cell == ' ':
                result_row.append(False)
            else:
                raise Exception("Bool mask must be made of '#' or <space> characters")
        result.append(result_row)
    return result


def helper_mask_string_to_numpy_bool_mask(str_rep):
    # assert even grid
    assert all([len(row) == len(str_rep[0]) for row in str_rep])
    # generate numpy array
    result = np.empty((len(str_rep), len(str_rep[0])), dtype='bool')
    for r, row in enumerate(str_rep):
        for c, cell in enumerate(row):
            if cell == "#":
                result[r, c] = True
            elif cell == ' ':
                result[r, c] = False
            else:
                raise Exception("Bool mask must be made of '#' or <space> characters")
    return result


def helper_grid_mask_to_string(grid_mask):
    buf = ""
    for row in grid_mask:
        for cell in row:
            buf += "#" if cell else " "
        buf += "\n"
    return buf

def helper_numpy_grid_mask_to_string(grid_mask):
    buf = ""
    for r in range(grid_mask.shape[0]):
        for c in range(grid_mask.shape[1]):
            buf += "#" if grid_mask[r,c] else " "
        buf += "\n"
    return buf


def helper_pretty_mask_compare(expected, result):
    # normalize types to List[List[bool]]
    if type(expected[0][0]) != bool:
        expected = helper_mask_string_to_bool_mask(expected)
    # Compare
    if len(expected) != len(result):
        print("Grids have different number of rows. Expected {}, Received {}".format(len(expected), len(result)))
        return False
    buf = "+" + "-" * len(expected[0]) + "+\n"
    any_difference = False
    for r in range(len(expected)):
        if len(expected[r]) != len(result[r]):
            print("Grids have different number of columns at row {}. Expected {}, Received {}".format(r, len(expected), len(result)))
            return False
        buf += '|'
        for c in range(len(expected[r])):
            e_cell = expected[r][c]
            r_cell = result[r][c]
            if e_cell and r_cell:
                buf += '#'
                continue
            if not e_cell and not r_cell:
                buf += ' '
                continue
            any_difference = True
            if e_cell:
                buf += COLOR_RED + '#' + COLOR_NONE
            else:
                buf += COLOR_GREEN + '#' + COLOR_NONE
        buf += '|\n'
    buf += "+" + "-" * len(expected[0]) + "+\n"
    print("\nDiff: Expected --> Result")
    print(buf)
    return not any_difference
    
    
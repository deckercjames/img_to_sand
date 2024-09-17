
import sys
from enum import Enum
from collections import namedtuple
from copy import deepcopy


class MoveDir(Enum):
    NORTH = 0,
    SOUTH = 1,
    EAST = 2,
    WEST = 3,

blob_contour_priority_dir_check = {
    MoveDir.NORTH: (
        (MoveDir.EAST,  (-1,  0)),
        (MoveDir.NORTH, (-1, -1)),
        (MoveDir.WEST,  None   ),
    ),
    MoveDir.SOUTH: (
        (MoveDir.WEST,  (0,  -1)),
        (MoveDir.SOUTH, (0,   0)),
        (MoveDir.EAST,  None   ),
    ),
    MoveDir.EAST: (
        (MoveDir.SOUTH, (0,  0)),
        (MoveDir.EAST,  (-1, 0)),
        (MoveDir.NORTH, None   ),
    ),
    MoveDir.WEST: (
        (MoveDir.NORTH, (-1, -1)),
        (MoveDir.WEST,  ( 0, -1)),
        (MoveDir.SOUTH, None   ),
    ),
}

def move_direction(current_pos, dir):
    if dir == MoveDir.NORTH:
        return (current_pos[0] - 1, current_pos[1])
    if dir == MoveDir.SOUTH:
        return (current_pos[0] + 1, current_pos[1])
    if dir == MoveDir.EAST:
        return (current_pos[0], current_pos[1] + 1)
    if dir == MoveDir.WEST:
        return (current_pos[0], current_pos[1] -1 )

def check_pixel(pixel_grid, r, c):
    if r < 0 or r >= len(pixel_grid):
        return 0
    if c < 0 or c >= len(pixel_grid[r]):
        return 0
    return pixel_grid[r][c]


def check_blob_mask_pixel(blob_mask, r, c):
    if r < 0 or r >= len(blob_mask):
        return False
    if c < 0 or c >= len(blob_mask[r]):
        return False
    return blob_mask[r][c]


def get_flood_fill_blob_mask(pixel_grid, r, c):
    pixel_stack = []
    pixel_stack.append((r, c))
    
    blob_color_index = pixel_grid[r][c]
    if blob_color_index == 0:
        return pixel_grid
    
    blob_mask = [[False for _ in range(len(row))] for row in pixel_grid]
    
    while len(pixel_stack) > 0:
        r, c = pixel_stack.pop()
        if r < 0 or r >= len(pixel_grid) or c < 0 or c >= len(pixel_grid[0]):
            continue
        # already visited
        if blob_mask[r][c]:
            continue
        # check if pixel should be included
        if check_pixel(pixel_grid, r, c) != blob_color_index:
            continue
        # expand pixel
        pixel_stack.append((r + 1, c))
        pixel_stack.append((r - 1, c))
        pixel_stack.append((r, c - 1))
        pixel_stack.append((r, c + 1))
        blob_mask[r][c] = True
    
    return blob_mask


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


def get_total_blob_mask(contour, num_rows, num_cols):
    
    # break the contour list into a grid of horizontal and vertical boundaries ("fences")
    hor_fences  = [[False for _ in range(num_cols)] for _ in range(num_rows + 1)]
    vert_fences = [[False for _ in range(num_cols + 1)] for _ in range(num_rows)]
    
    # populate fence tables
    for i, point in enumerate(contour):
        r, c = point
        prev_r, prev_c = get_list_element_cyclic(contour, i - 1)
        if r == prev_r:
            hor_fences[r][min(c, prev_c)] = True
        elif c == prev_c:
            vert_fences[min(r, prev_r)][c] = True
        else:
            raise Exception("Somethiing has gone horribally wrong")

    # Flood fill total blob using fences as restrictions
    
    total_blob_mask = [[False for _ in range(num_cols)] for _ in range(num_rows)]
    
    pixel_stack = []
    pixel_stack.append(contour[0])
    
    while len(pixel_stack) > 0:
        r, c = pixel_stack.pop()
        # already visited
        if r < 0 or r >= num_rows or c < 0 or c >= num_cols:
            continue
        if total_blob_mask[r][c]:
            continue
        # expand pixel
        if not hor_fences[r+1][c]:  pixel_stack.append((r + 1, c))
        if not hor_fences[r][c]:    pixel_stack.append((r - 1, c))
        if not vert_fences[r][c]:   pixel_stack.append((r, c - 1))
        if not vert_fences[r][c+1]: pixel_stack.append((r, c + 1))
        total_blob_mask[r][c] = True
    
    return total_blob_mask


def get_blob_outer_contour(blob_mask, r, c):
    contour = []
    contour.append((r, c))
    
    current_pos = (r, c+1)
    last_move_dir = MoveDir.EAST
    
    while True:
        if current_pos == (r, c):
            break
        for move_option in blob_contour_priority_dir_check[last_move_dir]:
            if move_option[1] is None:
                break
            check_location = (current_pos[0] + move_option[1][0], current_pos[1] + move_option[1][1])
            if check_blob_mask_pixel(blob_mask, check_location[0], check_location[1]):
                continue
            break
        contour.append(current_pos)
        current_pos = move_direction(current_pos, move_option[0])
        last_move_dir = move_option[0]
        pass
    
    return contour


def get_all_mask_contours(grid_mask):
    """
    Gets all the contours of a grid mask with positive "blobs".
    This can be used for getting the contours of a void within a blob
    There can be no nested mask contours
    """
    contours = []
    
    for r, row in enumerate(grid_mask):
        for c, cell in enumerate(row):
            if not grid_mask[r][c]:
                continue
            grid_blob_mask = get_flood_fill_blob_mask(grid_mask, r, c)
            grid_blob_contour = get_blob_outer_contour(grid_blob_mask, r, c)
            grid_mask = grid_mask_subtraction(grid_mask, grid_blob_mask)
            contours.append(grid_blob_contour)
    
    return contours


def grid_mask_subtraction(grid_mask, grid_mask_subtrahend):
    if len(grid_mask) != len(grid_mask_subtrahend):
        raise Exception("Can not subtract different sized masks")
    if len(grid_mask[0]) != len(grid_mask_subtrahend[0]):
        raise Exception("Can not subtract different sized masks")
        
    return [[(grid_mask[r][c] and not grid_mask_subtrahend[r][c]) for c in range(len(grid_mask[r]))] for r in range(len(grid_mask))]


BlobTuple = namedtuple("Blob", ["mask", "outer_contour", "void_contours", "sub_blobs"])

def get_blobs(pixel_grid, grid_mask=None):
    """
    Arguments:
        pixel_grid (2d list[int]): A grid of integers representing the color group of each pixel
    
    Returns (list(list(int, int))):
        A list of bound loops for each destinct color group blob
    """
    # No grid mask means the whole pixel grid is usable
    if grid_mask is None:
        grid_mask = [[True for _ in range(len(row))] for row in pixel_grid]
    
    blobs = []

    for r, row in enumerate(pixel_grid):
        for c, pixel in enumerate(row):
            if not grid_mask[r][c]:
                continue
            if pixel == 0:
                continue
            blob_mask = get_flood_fill_blob_mask(pixel_grid, r, c)
            blob_outer_contour = get_blob_outer_contour(blob_mask, r, c)
            total_blob_mask = get_total_blob_mask(blob_outer_contour, len(pixel_grid), len(pixel_grid[0]))
            # subtract the total blob mas from the current mask
            # we do not want to count this blob again and sub blobs will be found with the recursive call
            grid_mask = grid_mask_subtraction(grid_mask, total_blob_mask)
            sub_blob_mask = grid_mask_subtraction(total_blob_mask, blob_mask)
            void_contours = get_all_mask_contours(sub_blob_mask)
            sub_blobs = get_blobs(pixel_grid, grid_mask=sub_blob_mask)
            blob = BlobTuple(blob_mask, blob_outer_contour, void_contours, sub_blobs)
            blobs.append(blob)
            pass
    
    return blobs


def get_list_element_cyclic(list, i):
    return list[i % len(list)]


def main():
    pass

if __name__ == "__main__":
    sys.exit(main())
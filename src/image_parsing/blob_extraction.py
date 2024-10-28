
from enum import Enum
from collections import namedtuple

from src.utils import check_grid_element_safe
from src.utils import check_numpy_grid_element_safe
from src.utils import get_numpy_grid_mask_subtraction
from src.utils import get_list_element_cyclic

from src.tree import TreeNode
import numpy as np
import numpy.typing as npt


class Blob(namedtuple("Blob", ["outer_contour", "mask", "total_mask"])):
    def __eq__(self, other):
        if self.outer_contour != other.outer_contour:
            return False
        if type(self.mask) != type(other.mask) or type(self.mask) != type(other.mask):
            return False
        masks_equal = (self.mask == other.mask)
        total_masks_equal = (self.total_mask == other.total_mask)
        if type(self.mask) == np.ndarray:
            masks_equal = masks_equal.all()
        if type(self.total_mask) == np.ndarray:
            total_masks_equal = total_masks_equal.all()
        return masks_equal and total_masks_equal

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


def check_blob_mask_pixel(blob_mask, r, c):
    if r < 0 or r >= len(blob_mask):
        return False
    if c < 0 or c >= len(blob_mask[r]):
        return False
    return blob_mask[r][c]


def get_flood_fill_blob_mask(pixel_grid, r, c):
    pixel_stack = []
    pixel_stack.append((r, c))
    
    blob_color_index = pixel_grid[r, c]
    if blob_color_index == 0:
        return pixel_grid
    
    blob_mask = np.full(pixel_grid.shape, False, dtype='bool')
    
    while len(pixel_stack) > 0:
        r, c = pixel_stack.pop()
        if r < 0 or r >= pixel_grid.shape[0] or c < 0 or c >= pixel_grid.shape[1]:
            continue
        # already visited
        if blob_mask[r, c]:
            continue
        # check if pixel should be included
        if check_grid_element_safe(pixel_grid, r, c) != blob_color_index:
            continue
        # expand pixel
        pixel_stack.append((r + 1, c))
        pixel_stack.append((r - 1, c))
        pixel_stack.append((r, c - 1))
        pixel_stack.append((r, c + 1))
        blob_mask[r ,c] = True
    
    return blob_mask


def get_total_blob_mask(contour, num_rows, num_cols):
    
    # break the contour list into a grid of horizontal and vertical boundaries ("fences")
    hor_fences  = np.full((num_rows+1, num_cols), False, dtype='bool')
    vert_fences = np.full((num_rows, num_cols+1), False, dtype='bool')
    
    # populate fence tables
    for i, point in enumerate(contour):
        r, c = point
        prev_r, prev_c = get_list_element_cyclic(contour, i - 1)
        if r == prev_r:
            hor_fences[r, min(c, prev_c)] = True
        elif c == prev_c:
            vert_fences[min(r, prev_r), c] = True
        else:
            raise Exception("Somethiing has gone horribally wrong")

    # Flood fill total blob using fences as restrictions
    
    total_blob_mask = np.full((num_rows, num_cols), False, dtype='bool')
    
    pixel_stack = []
    pixel_stack.append(contour[0])
    
    while len(pixel_stack) > 0:
        r, c = pixel_stack.pop()
        # already visited
        if r < 0 or r >= num_rows or c < 0 or c >= num_cols:
            continue
        if total_blob_mask[r, c]:
            continue
        # expand pixel
        if not hor_fences[r+1, c]:  pixel_stack.append((r + 1, c))
        if not hor_fences[r, c]:    pixel_stack.append((r - 1, c))
        if not vert_fences[r, c]:   pixel_stack.append((r, c - 1))
        if not vert_fences[r, c+1]: pixel_stack.append((r, c + 1))
        total_blob_mask[r, c] = True
    
    return total_blob_mask


def get_blob_mask_outer_contour(blob_mask, r, c):
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
            if check_numpy_grid_element_safe(blob_mask, check_location[0], check_location[1], default=False):
                continue
            break
        contour.append(current_pos)
        current_pos = move_direction(current_pos, move_option[0])
        last_move_dir = move_option[0]
    
    return contour


def get_blob_tree_nodes_from_pixel_grid(pixel_grid, grid_mask=None):
    """
    Arguments:
        pixel_grid (2d list[int]): A grid of integers representing the color group of each pixel
    
    Returns (list(BlobTuple)):
        A list of bound loops for each destinct color group blob
    """
    # No grid mask means the whole pixel grid is usable
    if grid_mask is None:
        grid_mask = np.full(pixel_grid.shape, True, dtype='bool')
    
    blob_tree_nodes = []

    for r, c in np.ndindex(pixel_grid.shape):
        if not grid_mask[r, c]:
            continue
        if pixel_grid[r, c] == 0:
            continue
        blob_mask = get_flood_fill_blob_mask(pixel_grid, r, c)
        blob_outer_contour = get_blob_mask_outer_contour(blob_mask, r, c)
        total_blob_mask = get_total_blob_mask(blob_outer_contour, len(pixel_grid), len(pixel_grid[0]))
        # subtract the total blob mas from the current mask
        # we do not want to count this blob again and sub blobs will be found with the recursive call
        grid_mask = get_numpy_grid_mask_subtraction(grid_mask, total_blob_mask)
        sub_blob_mask = get_numpy_grid_mask_subtraction(total_blob_mask, blob_mask)
        sub_blob_tree_nodes = get_blob_tree_nodes_from_pixel_grid(pixel_grid, grid_mask=sub_blob_mask)
        blob = Blob(blob_outer_contour, blob_mask, total_blob_mask)
        blob_tree_node = TreeNode(blob, sub_blob_tree_nodes)
        blob_tree_nodes.append(blob_tree_node)
    
    return blob_tree_nodes


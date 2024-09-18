
from src.utils import check_grid_element_safe
from src.blob_extraction import get_blob_mask_outer_contour
from src.utils import grid_mask_subtraction
from src.utils import grid_mask_to_str


def get_flood_fill_grid_mask(grid_mask, start_r, start_c):
    cell_stack = []
    cell_stack.append((start_r, start_c))

    grid_blob_mask = [[False for _ in range(len(row))] for row in grid_mask]
    
    while len(cell_stack) > 0:
        r, c = cell_stack.pop()
        if r < 0 or r >= len(grid_mask) or c < 0 or c >= len(grid_mask[0]):
            continue
        # already visited
        if grid_blob_mask[r][c]:
            continue
        # check if pixel should be included
        if not grid_mask[r][c]:
            continue
        # expand pixel
        cell_stack.append((r + 1, c))
        cell_stack.append((r - 1, c))
        cell_stack.append((r, c - 1))
        cell_stack.append((r, c + 1))
        grid_blob_mask[r][c] = True
    
    return grid_blob_mask


def get_all_mask_contours(grid_mask):
    """
    Gets all the contours of a grid mask with positive "blobs".
    This can be used for getting the contours of a void within a blob
    There can be no nested mask contours
    """
    contours = []
    
    for r in range(len(grid_mask)):
        for c in range(len(grid_mask[0])):
            if not grid_mask[r][c]:
                continue
            grid_blob_mask = get_flood_fill_grid_mask(grid_mask, r, c)
            grid_blob_contour = get_blob_mask_outer_contour(grid_blob_mask, r, c)
            grid_mask = grid_mask_subtraction(grid_mask, grid_blob_mask)
            contours.append(grid_blob_contour)
    
    return contours



def get_blob_topography(blob):
    
    # Get the void regions
    
    pass


def get_topography(blobs):
    pass

from PIL import Image

from src.utils import check_grid_element_safe
from src.utils import get_numpy_grid_mask_union

from src.pbar import ProgressBar

import logging
import sys
import numpy as np

def load_image(image_path):
    
    try:
        with Image.open(image_path).convert("RGBA") as image_fp:
            return np.array(image_fp)
    except OSError as e:
        logging.fatal("Could not load image '{}'. {}".format(image_path, e))
        sys.exit(1)
        
    # print("Got image {}x{}", image_height, image_width)
    
    # print(pixels[0][0])
    
    # count the number of colors
    # colors = set()
    # for row in pixels:
    #     colors.update(row)
    # print("Num colors ", len(colors))
    # print(colors)
    
    return pixels



def colors_similar(c0, c1, distance_threshold=0.2):
    
    dist_squared = 0
    for v0, v1 in zip(c0, c1):
        dist_squared += (int(v0) - int(v1)) ** 2
        
    return dist_squared < (distance_threshold * 255) ** 2
    

def get_flood_fill_blob_mask(pixel_grid, r, c):
    pixel_stack = []
    pixel_stack.append((r, c))
    
    reference_color = pixel_grid[r, c, :]
    
    blob_mask = np.full(pixel_grid.shape[0:2], False, dtype='bool')
    
    while len(pixel_stack) > 0:
        r, c = pixel_stack.pop()
        if r < 0 or r >= pixel_grid.shape[0] or c < 0 or c >= pixel_grid.shape[1]:
            continue
        # already visited
        if blob_mask[r, c]:
            continue
        # check if pixel should be included
        current_color = check_grid_element_safe(pixel_grid, r, c, default=None)
        if current_color is None:
            continue
        if not colors_similar(current_color, reference_color):
            continue
        # expand pixel
        pixel_stack.append((r + 1, c))
        pixel_stack.append((r - 1, c))
        pixel_stack.append((r, c - 1))
        pixel_stack.append((r, c + 1))
        # pixel_stack.append((r - 1, c - 1))
        # pixel_stack.append((r - 1, c + 1))
        # pixel_stack.append((r + 1, c - 1))
        # pixel_stack.append((r + 1, c + 1))
        blob_mask[r, c] = True
    
    return blob_mask



def enumerate_pixels(raw_pixel_grid, min_blob_size=20):
    
    enumerated_pixel_grid = np.full(raw_pixel_grid.shape[0:2], 0)
    pixel_enumeration_index = 1
    
    visited_mask = np.full(raw_pixel_grid.shape[0:2], False, dtype='bool')
    
    num_rows = raw_pixel_grid.shape[0]
    num_cols = raw_pixel_grid.shape[1]
    
    pbar = ProgressBar(num_rows*num_cols)
    
    for r in range(num_rows):
        for c in range(num_cols):
            pbar.update()
            if visited_mask[r, c]:
                continue
            similar_color_blob_mask = get_flood_fill_blob_mask(raw_pixel_grid, r, c)
            visited_mask = get_numpy_grid_mask_union(visited_mask, similar_color_blob_mask)
            
            # count the number of pixels in this blob to see if it enough to warrent consideration
            blob_pixel_count = 0
            for row in similar_color_blob_mask:
                for cell in row:
                    if cell:
                        blob_pixel_count += 1

            if blob_pixel_count < min_blob_size:
                continue
                
            # Check if this is background or not
            idx = pixel_enumeration_index
            if colors_similar((255, 255, 255, 255), raw_pixel_grid[r, c, :]) or raw_pixel_grid[r, c, 3] < 10:
                idx = 0
    
            # set the pixels in the enumerated pixel mask
            for r1 in range(len(similar_color_blob_mask)):
                for c1 in range(len(similar_color_blob_mask[0])):
                    if similar_color_blob_mask[r1, c1]:
                        enumerated_pixel_grid[r1, c1] = idx
            
            if idx != 0:
                pixel_enumeration_index += 1
    
    pbar.complete()
            
    # print(grid_mask_to_str(visited_mask))
    
    # print("Pixels enumerated. {} uniqe".format(pixel_enumeration_index-1))
    
    # buf = ""
    # for r in range(len(enumerated_pixel_grid)):
    #     for c in range(len(enumerated_pixel_grid[0])):
    #         buf += str(enumerated_pixel_grid[r][c])
    #     buf += "\n"
    # print(buf)
    
    return enumerated_pixel_grid
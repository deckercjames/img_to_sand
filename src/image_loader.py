
from PIL import Image

from src.utils import check_grid_element_safe
from src.utils import get_grid_mask_union
from src.utils import grid_mask_to_str


def load_image(image_path):
    
    try:
        with Image.open(image_path).convert("RGBA") as image_fp:
            image_width, image_height = image_fp.size
            pixels = []
            for r in range(image_height):
                pixel_row = []
                for c in range(image_width):
                    # print(image_fp.getpixel((c, r)))
                    pixel_row.append(image_fp.getpixel((c, r)))
                pixels.append(pixel_row)
    except OSError:
        print("Fail")
        return
        
    print("Got image {}x{}", image_height, image_width)
    
    print(pixels[0][0])
    
    # count the number of colors
    colors = set()
    for row in pixels:
        colors.update(row)
    print("Num colors ", len(colors))
    print(colors)
    
    return pixels



def colors_similar(c0, c1, distance_threshold=0.2):
    
    dist_squared = 0
    for v0, v1 in zip(c0, c1):
        dist_squared += (v0 - v1) ** 2
    
    return dist_squared < (distance_threshold * 255) * 2
    

def get_flood_fill_blob_mask(pixel_grid, r, c):
    pixel_stack = []
    pixel_stack.append((r, c))
    
    reference_color = pixel_grid[r][c]
    
    blob_mask = [[False for _ in range(len(row))] for row in pixel_grid]
    
    while len(pixel_stack) > 0:
        r, c = pixel_stack.pop()
        if r < 0 or r >= len(pixel_grid) or c < 0 or c >= len(pixel_grid[0]):
            continue
        # already visited
        if blob_mask[r][c]:
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
        blob_mask[r][c] = True
    
    return blob_mask



def enumerate_pixels(raw_pixel_grid, min_blob_size=20):
    
    enumerated_pixel_grid = [[0 for _ in range(len(row))] for row in raw_pixel_grid]
    pixel_enumeration_index = 1
    
    visited_mask = [[False for _ in range(len(row))] for row in raw_pixel_grid]
    
    print("Enumerating")
    
    for r in range(len(raw_pixel_grid)):
        for c in range(len(raw_pixel_grid[0])):
            if visited_mask[r][c]:
                continue
            similar_color_blob_mask = get_flood_fill_blob_mask(raw_pixel_grid, r, c)
            visited_mask = get_grid_mask_union(visited_mask, similar_color_blob_mask)
            
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
            if colors_similar((255, 255, 255, 255), raw_pixel_grid[r][c]) or raw_pixel_grid[r][c][3] < 10:
                idx = 0
    
            # set the pixels in the enumerated pixel mask
            for r1 in range(len(similar_color_blob_mask)):
                for c1 in range(len(similar_color_blob_mask[0])):
                    if similar_color_blob_mask[r1][c1]:
                        enumerated_pixel_grid[r1][c1] = idx
            
            if idx != 0:
                pixel_enumeration_index += 1
            
    print(grid_mask_to_str(visited_mask))
    
    print("Pixels enumerated. {} uniqe".format(pixel_enumeration_index-1))
    
    buf = ""
    for r in range(len(enumerated_pixel_grid)):
        for c in range(len(enumerated_pixel_grid[0])):
            buf += str(enumerated_pixel_grid[r][c])
        buf += "\n"
    print(buf)
    
    return enumerated_pixel_grid
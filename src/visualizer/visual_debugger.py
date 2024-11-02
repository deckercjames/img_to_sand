
from PIL import Image, ImageDraw

from src.linker.linker_problem import LinkerProblem
from src.linker.linker_problem import LinkerSearchState
from typing import List
import os

import logging
import numpy as np

def dump_grid_mask(grid_mask, image_name):
    img = Image.new("RGB", (grid_mask.shape[1], grid_mask.shape[0]))
    img_draw = ImageDraw.Draw(img)
    
    for r,c in np.ndindex(grid_mask.shape):
        if grid_mask[r,c]:
            color = 'black'
        else:
            color = 'white'
        
        img_draw.point((c,r), fill=color)
    
    img.save("debug_output/{}.png".format(image_name))


def dump_enumerated_pixels(pixel_grid):
    
    dir = "debug_output/enum_pixels/"
    if not os.path.isdir(dir):
        os.mkdir(dir)
    
    img_shape = (pixel_grid.shape[1], pixel_grid.shape[0])
    
    colors = ['white', 'red', 'blue', 'orange', 'purple', 'green', 'yellow', 'black']
    
    img = Image.new("RGB", img_shape)
    img_draw = ImageDraw.Draw(img)
    
    for r,c in np.ndindex(pixel_grid.shape):
        
        color_index = min(pixel_grid[r,c], len(colors) - 1)
        
        img_draw.point((c,r), fill=colors[color_index])
        
    img.save("debug_output/enum_pixels/{}.png".format("all_blobs"))


def dump_raw_pixels(raw_pixel_grid):
    
    dir = "debug_output/enum_pixels/"
    if not os.path.isdir(dir):
        os.mkdir(dir)
    
    num_rows = raw_pixel_grid.shape[0]
    num_cols = raw_pixel_grid.shape[1]
    
    img_shape = (num_cols, num_rows)
    
    img = Image.new("RGB", img_shape)
    img_draw = ImageDraw.Draw(img)
    
    for r in range(num_rows):
        for c in range(num_cols):
            
            color = tuple([int(raw_pixel_grid[r,c,k]) for k in range(4)])
        
            img_draw.point((c,r), fill=color)
        
    img.save("debug_output/enum_pixels/{}.png".format("raw_pixels"))

    
    


def dump_linker_open_list(problem: LinkerProblem, open_list: List[LinkerSearchState], itteration: int):
    
    dir = "debug_output/linker_fringe_itter_{}/".format(itteration)
    if not os.path.isdir(dir):
        os.mkdir(dir)
    
    for i, (_, search_state) in enumerate(open_list):
        img = Image.new("RGB", (problem.get_num_cols()+3, problem.get_num_rows()+3))
        img_draw = ImageDraw.Draw(img)
        
        if itteration > 0:
            # Draw last link
            last_link = [(c+1,r+1) for r,c in search_state.path[-1].entity_linkage_points]
            img_draw.line(last_link, fill="#baa800", width = 0)
            
            # draw all previous links
            for path_item in search_state.path[:-1]:
                prev_link = [(c+1,r+1) for r,c in path_item.entity_linkage_points]
                img_draw.line(prev_link, fill="grey", width = 0)
        
        # draw all blobs
        for r in range(len(problem.total_image_mask)):
            for c in range(len(problem.total_image_mask[0])):
                if not problem.total_image_mask[r][c]:
                    continue
                img_draw.point((c+1,r+1), fill="white")

        # grey out visited blobs
        for r in range(len(search_state.visited_mask)):
            for c in range(len(search_state.visited_mask[0])):
                if not search_state.visited_mask[r][c]:
                    continue
                img_draw.point((c+1,r+1), fill="grey")
    
        # highlight current blob
        if search_state.cur_entity_ref.entity_idx != None:
            cur_blob_mask = problem.layers[search_state.cur_entity_ref.layer_idx][search_state.cur_entity_ref.entity_idx].get_entity_grid_mask()
            for r in range(len(cur_blob_mask)):
                for c in range(len(cur_blob_mask[0])):
                    if not cur_blob_mask[r][c]:
                        continue
                    img_draw.point((c+1,r+1), fill="#baa800")
        else:
            border = [(0,0), (0,problem.get_num_rows()+2), (problem.get_num_cols()+2,problem.get_num_rows()+2), (problem.get_num_cols()+2,0), (0,0)]
            img_draw.line(border, fill="#baa800")
        
        img.save("{}/state_cost_{:05}+{:02}_.png".format(dir, int(search_state.cost_to_state), i))
        


def export_path_to_image(path, num_rows, num_cols, output_file_path):
    
    img = Image.new("RGB", (num_cols+1, num_rows+1))
    
    # Transpose all path points
    path = [(c,r) for r,c in path]
    
    img_draw = ImageDraw.Draw(img)   
    img_draw.line(path, fill="#baa800", width = 0)
    
    try:
        img.save(output_file_path)
    except OSError as err:
        logging.error("Failed to write visualizer output '{}'. {}".format(path, err))

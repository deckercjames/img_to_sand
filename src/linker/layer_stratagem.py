
from src.linker.zhang_suen import get_split_lines_and_blobs
from src.utils import get_grid_mask_subtraction
from src.linker.linkable_entity.topography import get_mask_with_inward_bleed
from src.linker.linkable_entity.topography import get_all_blobs_from_mask
from src.linker.linkable_entity.linkable_entity_line import get_line_linkable_entity
from src.linker.linkable_entity.linkable_entity_blob import get_blob_linkable_entity
from typing import List
from src.linker.linkable_entity.topography import get_flood_fill_grid_mask
from src.pbar import ProgressBar

from src.linker.linkable_entity.linkable_entity import LinkableEntity


def get_all_separate_grid_masks(grid_mask):
    
    separate_grid_masks = []
    
    num_rows = len(grid_mask)
    num_cols = len(grid_mask[0])
    
    for r in range(num_rows):
        for c in range(num_cols):
            if not grid_mask[r][c]:
                continue
            separate_grid_mask = get_flood_fill_grid_mask(grid_mask, r, c, diag=True)
            separate_grid_masks.append(separate_grid_mask)
            grid_mask = get_grid_mask_subtraction(grid_mask, separate_grid_mask)
            
    return separate_grid_masks


def get_all_linkable_entities_for_blob_layer(blob_layer, num_line_errosion_itterations: int, num_blob_buffer_itterations: int, pbar: ProgressBar):
    
    all_linkable_entities = []
    
    pbar.push_subproblem(len(blob_layer))
    
    for blob in blob_layer:
        micro_blobs_grid_mask, lines_grid_mask = get_split_lines_and_blobs(blob.mask, num_line_errosion_itterations)
        
        # print("ITTER")
        # print("Current length of all_linkable_entities "+str(len(all_linkable_entities)))
        # print("micro blobs mask")
        # print(grid_mask_to_str(micro_blobs_grid_mask))
        # print("line grid mask")
        # print(grid_mask_to_str(lines_grid_mask))
        
        # Handle lines from blob
        line_grid_masks = get_all_separate_grid_masks(lines_grid_mask)
        # print("num lines "+str(len(line_grid_masks)))
        for line_grid_mask in line_grid_masks:
            # print("line itter")
            all_linkable_entities.append(get_line_linkable_entity(line_grid_mask))
        
        # Handle micro blobs from blob
        for _ in range(num_blob_buffer_itterations):
            micro_blobs_grid_mask = get_mask_with_inward_bleed(micro_blobs_grid_mask, diag_bleed=True)
        
        # print("micro blobs mask")
        # print(grid_mask_to_str(micro_blobs_grid_mask))
        micro_blobs = get_all_blobs_from_mask(micro_blobs_grid_mask)
        
        # print("num micro blobs "+str(len(micro_blobs)))
        for micro_blob in micro_blobs:
            # print("blob itter")
            all_linkable_entities.append(get_blob_linkable_entity(micro_blob))
        
        pbar.update()
    
    pbar.complete_subproblem()
    
    return all_linkable_entities


def get_all_layer_stratagem(blob_layers, num_line_errosion_itterations: int, num_blob_buffer_itterations: int) -> List[List[LinkableEntity]]:
    
    layer_stratagems = []
    
    pbar = ProgressBar(len(blob_layers))

    for blobs_in_layer in blob_layers:
        # get all linkable entities
        layer_linkable_entities = get_all_linkable_entities_for_blob_layer(blobs_in_layer, num_line_errosion_itterations, num_blob_buffer_itterations, pbar)
        # Add layer stratagem to list
        layer_stratagems.append(layer_linkable_entities)
        pbar.update()
    
    pbar.complete()
    
    # must reverse the layers before returning them since they were build backward
    return layer_stratagems
        
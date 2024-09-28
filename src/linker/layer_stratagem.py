

from collections import namedtuple

from src.zhang_suen import get_split_lines_and_blobs
from src.utils import get_all_false_mask
from src.utils import get_grid_mask_union
from src.topography import get_mask_with_inward_bleed
from src.topography import get_all_blobs_from_mask
from src.topography import get_blob_topography
from src.blob_extraction import get_flood_fill_blob_mask
from src.linker.linkable_entity import get_line_linkable_entity
from src.linker.linkable_entity import get_blob_linkable_entity
from dataclasses import dataclass
from typing import List, Set

from src.linker.linkable_entity import LinkableEntity

@dataclass
class LayerStratagem:
    scratch_mask: List[List[bool]]
    linkable_entities: List[LinkableEntity]
"""
scratch_mask: The unioned mask of all linkable entities in the same layer and subsequent layers
              This reprersents places that it is ok to use to make the link because they will
              over-drawn later.
linkagle_entities list(LinkableEntity): All linkable entities from this layer
"""


def get_all_linkable_entities_for_blob_layer(blob_layer, num_line_errosion_itterations, num_blob_buffer_itterations):
    
    all_linkable_entities = []
    
    for blob in blob_layer.blobs:
        micro_blobs_grid_mask, lines_grid_mask = get_split_lines_and_blobs(blob.mask, num_line_errosion_itterations)
        
        # Handle lines from blob
        line_blobs = get_all_blobs_from_mask(lines_grid_mask)
        for line_blob in line_blobs:
            all_linkable_entities.append(get_line_linkable_entity(line_blob))
        
        # Handle micro blobs from blob
        for _ in range(num_blob_buffer_itterations):
            micro_blobs_grid_mask = get_mask_with_inward_bleed(micro_blobs_grid_mask, diag_bleed=True)
        
        micro_blobs = get_all_blobs_from_mask(micro_blobs_grid_mask)
        
        for micro_blob in micro_blobs:
            all_linkable_entities.append(get_blob_linkable_entity(micro_blob))
    
    return all_linkable_entities


def get_all_layer_stratagem(blob_layers, num_line_errosion_itterations, num_blob_buffer_itterations):
    
    layer_stratagems = []
    
    scratch_mask = get_all_false_mask(len(blob_layers[0].mask), len(blob_layers[0].mask[0]))
    
    for blobs_in_layer in reversed(blob_layers):
        # get all linkable entities
        all_linkable_entities = get_all_linkable_entities_for_blob_layer(blobs_in_layer, num_line_errosion_itterations, num_blob_buffer_itterations)
        # add all blob masks to the scrath mask
        for blob in blobs_in_layer:
            scratch_mask = get_grid_mask_union(blob.mask)
        # Add layer stratagem to list
        layer_stratagems.append(LayerStratagem(scratch_mask, all_linkable_entities))
    
    # must reverse the layers before returning them since they were build backward
    return reversed(layer_stratagems)
        

from src.linker.layer_stratagem import get_all_layer_stratagem
from src.linker.layer_stratagem import LayerStratagem
from collections import namedtuple
from src.utils import get_all_false_mask
import heapq
from typing import List, Set
from copy import deepcopy
from dataclasses import dataclass
from src.utils import get_grid_mask_union

PathItem = namedtuple("PathItem", ["prev_entity_exit_point", "next_entity_ref", "next_entity_entry_point"])
EntityReference = namedtuple("EntityReference", ["layer_idx", "entity_idx"])

@dataclass
class LinkerSearchState:
    cur_entity_ref: EntityReference
    visited_mask: List[List[bool]]
    visited_layer_entity_idx_set: Set[int]
    cost_to_state: float
    path: List[PathItem]
"""
cur_entity_ref (EntityReference): contains the layer index, entity_index of the current entity. None means edge
visited_mask (gridmask): The union of all masks of visited entities. This prevents us from making a link that
                         traverses across a completed entity
"""


def get_entity_link(e0, e1):
    pass


def is_goal_state(layers, search_state) -> bool:
    cur_entity_ref = search_state.cur_entity_ref
    return cur_entity_ref.layer_idx == len(layers) - 1 and cur_entity_ref.entity_idx == len(layers.linkable_entities) - 1

def get_child_states(layers: List[LayerStratagem], current_state: LinkerSearchState) -> List[LinkerSearchState]:
    
    next_layer_idx = current_state.cur_entity_ref.layer_idx
    next_visited_layer_entity_idx_set = current_state.visited_layer_entity_idx_set
    
    # Check if this layer is complete
    if len(current_state.visited_layer_entity_idx_set) == len(layers[current_state.cur_entity_ref.layer_idx].linkable_entities):
        # Move to next layer
        next_layer_idx += 1
        next_visited_layer_entity_idx_set = set()
    
    child_states = []
        
    # For every unvisited entity in the next layer (next layer could be the current layer)
    for linkable_entity_idx, linkable_entity in enumerate(layers[next_layer_idx].linkable_entities):
        # If visited, ignore
        if linkable_entity_idx in current_state.visited_layer_entity_idx_set:
            continue
        # Update the visited set for this child
        child_visited_layer_entity_idx_set = next_visited_layer_entity_idx_set.copy()
        child_visited_layer_entity_idx_set.add(linkable_entity_idx)
        # Get the path item and the cost
        link_cost, link_path_item = get_entity_link(current_state.cur_entity_ref, linkable_entity)
        child_state = LinkerSearchState(
            EntityReference(next_layer_idx, linkable_entity_idx),
            get_grid_mask_union(current_state.visited_mask, linkable_entity.get_entity_grid_mask()),
            child_visited_layer_entity_idx_set,
            current_state.cost_to_state + link_cost,
            link_path_item
        )
        child_states.append(child_state)
    
    pass


def get_heuristic_for_state(layers, state):
    pass


def get_linked_path(blob_layers, num_line_errosion_itterations, num_blob_buffer_itterations):
    
    layers = get_all_layer_stratagem(blob_layers, num_line_errosion_itterations, num_blob_buffer_itterations)
    
    start_state = LinkerSearchState(
        None,
        get_all_false_mask(len(blob_layers[0].blobs[0].mask), len(blob_layers[0].blobs[0].mask[0])),
        set(),
        0,
        []
    )
    
    fringe = []
    heapq.heappush(fringe, (0, start_state))
    
    while len(fringe) > 0:
        
        # Pop next state
        _, current_state = heapq.heappop(fringe)
        
        # Check goal state
        if is_goal_state(current_state):
            return current_state.path
        
        # Expand children
        for child_state in get_child_states(current_state):
            new_f = child_state.cost + get_heuristic_for_state(child_state)
            heapq.heappush(fringe, (new_f, child_state))
    
    raise Exception("Linker Failed To Find Path")

from collections import namedtuple
from dataclasses import dataclass
from src.linker.linkable_entity.linkable_entity import LinkableEntity
from typing import List, Set
from src.linker.linkable_entity.linkable_entity import EntityReference

@dataclass
class CostMenu:
    # Something already drawn
    visited_mask_cost: int
    # Something that will be covered later
    future_mask_cost: int
    # Basic cost
    base_cost: int

@dataclass
class LinkerProblem:
    layers: List[List[LinkableEntity]]
    total_image_mask: List[List[bool]]
    cost_menu: CostMenu
    def get_num_rows(self):
        return len(self.total_image_mask)
    def get_num_cols(self):
        return len(self.total_image_mask[0])
    def get_total_num_entities_to_link(self):
        return sum([len(layer) for layer in self.layers])
    

PathItem = namedtuple("PathItem", ["entity_linkage_points", "next_entity_ref"])

@dataclass
class LinkerSearchState:
    cur_entity_ref: EntityReference
    visited_mask: List[List[bool]]
    visited_layer_entity_idx_set: Set[int]
    cost_to_state: float
    path: List[PathItem]
    def __lt__(self, other):
        return True
"""
cur_entity_ref (EntityReference): contains the layer index, entity_index of the current entity. None means edge
visited_mask (gridmask): The union of all masks of visited entities. This prevents us from making a link that
                         traverses across a completed entity
"""

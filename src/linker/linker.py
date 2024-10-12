
from src.linker.layer_stratagem import get_all_layer_stratagem
from collections import namedtuple
from src.utils import get_all_false_mask
import heapq
from typing import List, Set
from copy import deepcopy
from dataclasses import dataclass
from src.utils import get_grid_mask_union
from src.linker.linkable_entity.linkable_entity import LinkableEntity
from src.linker.linkable_entity.linkable_entity import EntityReference
from src.utils import check_grid_element_safe
from src.linker.get_children import get_child_states
from src.linker.linker_problem import *

entity_link_cache = {}


def is_goal_state(problem: LinkerProblem, search_state) -> bool:
    cur_entity_ref = search_state.cur_entity_ref
    return cur_entity_ref.layer_idx == len(problem.layers) - 1 and cur_entity_ref.entity_idx == len(problem.layers[cur_entity_ref.layer_idx]) - 1



def get_heuristic_for_state(layers, state):
    return 0


def get_linked_path(problem: LinkerProblem):
    
    start_state = LinkerSearchState(
        None,
        get_all_false_mask(problem.get_num_rows(), problem.get_num_cols()),
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
        for child_state in get_child_states(problem, current_state, 5):
            new_f = child_state.cost + get_heuristic_for_state(child_state)
            heapq.heappush(fringe, (new_f, child_state))
        
        # Enforce beam limit
        new_fringe = []
        for _ in range(10):
            new_fringe.append(heapq.heappop(fringe))
        fringe = new_fringe
    
    raise Exception("Linker Failed To Find Path")
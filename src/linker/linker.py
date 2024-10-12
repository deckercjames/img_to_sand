
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


def is_goal_state(problem: LinkerProblem, search_state: LinkerSearchState) -> bool:
    cur_entity_ref = search_state.cur_entity_ref
    # print("Layer check {} == ({} - 1)".format(cur_entity_ref.layer_idx, len(problem.layers)))
    # print("entity check {} == {}".format(len(search_state.visited_layer_entity_idx_set), len(problem.layers[cur_entity_ref.layer_idx])))
    return cur_entity_ref.layer_idx == len(problem.layers) - 1 and len(search_state.visited_layer_entity_idx_set) == len(problem.layers[cur_entity_ref.layer_idx])



def get_heuristic_for_state(problem: LinkerProblem, search_state: LinkerSearchState):
    return 0


def get_single_linked_path(problem: LinkerProblem, max_children_pre_expansion: int, beam_width: int):
    
    start_state = LinkerSearchState(
        EntityReference(0, None),
        get_all_false_mask(problem.get_num_rows(), problem.get_num_cols()),
        set(),
        0,
        []
    )
    
    fringe = []
    heapq.heappush(fringe, (0, start_state))
    
    itter_cnt = 0
    while True:
        next_fringe = []
        
        print("expanding fringe, length="+str(len(fringe))+", itteration="+str(itter_cnt))
        itter_cnt += 1
        
        while len(fringe) > 0:
            
            # Pop next state
            _, current_state = heapq.heappop(fringe)
            
            if current_state.cur_entity_ref.entity_idx is None:
                print("  expanding child [border], remaining fringe length="+str(len(fringe)))
            else:
                print("  expanding child [entity], remaining fringe length="+str(len(fringe)))
            
            # print("\n\nCurrentState {")
            # print("  current_entity_ref: {}".format(str(current_state.cur_entity_ref)))
            # print("  visited_layer_entity_idx_set: {}".format(str(current_state.visited_layer_entity_idx_set)))
            # print("  ...\n}")
    
            
            # Check goal state
            if is_goal_state(problem, current_state):
                return current_state.path
            
            # Expand children
            for child_state in get_child_states(problem, current_state, max_children_pre_expansion):
                new_f = child_state.cost_to_state + get_heuristic_for_state(problem, child_state)
                heapq.heappush(next_fringe, (new_f, child_state))
            
        # Enforce beam limit
        while len(next_fringe) > 0 and len(fringe) < beam_width:
            heapq.heappush(fringe, heapq.heappop(next_fringe))
        
        # Failed to find goal
        if len(fringe) == 0:
            break
    
    raise Exception("Linker Failed To Find Path")


def get_linked_path(layers):
    
    total_image_mask = deepcopy(layers[0][0].get_entity_grid_mask())
    for layer in layers:
        for entity in layer:
            total_image_mask = get_grid_mask_union(total_image_mask, entity.get_entity_grid_mask())
    
    problem = LinkerProblem(
        layers=layers,
        total_image_mask=total_image_mask,
        cost_menu=CostMenu(
            visited_mask_cost=10000,
            future_mask_cost=1,
            base_cost=10,
        )
    )
    
    return get_single_linked_path(problem, 5, 10)
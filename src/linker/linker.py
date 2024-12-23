
from src.utils import get_all_false_mask
import heapq
from src.utils import get_numpy_grid_mask_union
from src.linker.linkable_entity.linkable_entity import EntityReference
from src.linker.get_children import get_child_states
from src.linker.linker_problem import *
import multiprocessing
import numpy as np

from src.pbar import ProgressBar
from src.visualizer.visual_debugger import dump_linker_open_list
import random

entity_link_cache = {}


def is_goal_state(problem: LinkerProblem, search_state: LinkerSearchState) -> bool:
    cur_entity_ref = search_state.cur_entity_ref
    # print("Layer check {} == ({} - 1)".format(cur_entity_ref.layer_idx, len(problem.layers)))
    # print("entity check {} == {}".format(len(search_state.visited_layer_entity_idx_set), len(problem.layers[cur_entity_ref.layer_idx])))
    return cur_entity_ref.layer_idx == len(problem.layers) - 1 and len(search_state.visited_entity_ref_set) == sum([len(layer) for layer in problem.layers])



def get_bounding_box_to_border(problem: LinkerProblem, entity_ref: EntityReference):
    
    entity_bounding_box = problem.layers[entity_ref.layer_idx][entity_ref.entity_idx].get_bounding_box()
    
    return min(
        entity_bounding_box[0],
        entity_bounding_box[1],
        problem.get_num_rows() - entity_bounding_box[2],
        problem.get_num_cols() - entity_bounding_box[3],
    )

def get_dist_between_bounding_boxes(problem: LinkerProblem, entity_ref_0: EntityReference, entity_ref_1: EntityReference):
    
    entity_bounding_box_0 = problem.layers[entity_ref_0.layer_idx][entity_ref_0.entity_idx].get_bounding_box()
    entity_bounding_box_1 = problem.layers[entity_ref_1.layer_idx][entity_ref_1.entity_idx].get_bounding_box()
    
    return min(
        entity_bounding_box_1[2] - entity_bounding_box_0[0],
        entity_bounding_box_1[3] - entity_bounding_box_0[1],
        entity_bounding_box_0[2] - entity_bounding_box_1[0],
        entity_bounding_box_0[3] - entity_bounding_box_1[1],
    )



def get_heuristic_for_state(problem: LinkerProblem, search_state: LinkerSearchState):
    
    # make an array of all un-visited entities
    all_unvisited_entites = []
    for layer_idx in range(len(problem.layers)):
        for entity_idx in range(len(problem.layers)):
            entity_ref = EntityReference(layer_idx, entity_idx)
            if entity_ref in search_state.visited_entity_ref_set:
                continue
            all_unvisited_entites.append(entity_ref)
    
    # get a random set n of them to use
    SAMPLE_SIZE = 5
    shuffle_idx = 0
    while shuffle_idx < SAMPLE_SIZE:
        if shuffle_idx >= len(all_unvisited_entites) - 1:
            break
        swap_with_idx = random.randint(shuffle_idx + 1, len(all_unvisited_entites) - 1)
        temp = all_unvisited_entites[shuffle_idx]
        all_unvisited_entites[shuffle_idx] = all_unvisited_entites[swap_with_idx]
        all_unvisited_entites[swap_with_idx] = temp
        shuffle_idx += 1
    all_unvisited_entites_sample = all_unvisited_entites[:SAMPLE_SIZE]
    
    min_dist = get_bounding_box_to_border(problem, entity_ref)
        
    # Calculate a cost based on the entity
    for entity_ref in all_unvisited_entites_sample:
        
        # compare against all other entities
        for other_entity_ref in all_unvisited_entites:
            dist = get_dist_between_bounding_boxes(problem, entity_ref, other_entity_ref)
            min_dist = min(min_dist, dist)

    return min_dist


def expand_linker_search_state(problem: LinkerProblem, current_state: LinkerSearchState, max_children_per_expansion: int):
    if is_goal_state(problem, current_state):
        return current_state, None
    
    child_fringe = []

    # Expand children
    for child_state in get_child_states(problem, current_state, max_children_per_expansion):
        heuristic = get_heuristic_for_state(problem, child_state)
        new_f = child_state.cost_to_state + (heuristic * 2)
        child_fringe.append((new_f, child_state))
    
    return None, child_fringe
                


def get_single_linked_path(problem: LinkerProblem, max_children_per_expansion: int, beam_width: int, heuristic_weight: float):
    
    start_state = LinkerSearchState(
        EntityReference(0, None),
        np.full(problem.total_image_mask.shape, False, dtype='bool'),
        set(),
        0,
        []
    )
    
    fringe = []
    heapq.heappush(fringe, (0, start_state))
    
    pbar = ProgressBar(problem.get_total_num_entities_to_link() * 2)
    itter_cnt = 0
    dump_linker_open_list(problem, fringe, itter_cnt)
    
    pool = multiprocessing.Pool(processes=(multiprocessing.cpu_count() - 1))
    while True:
        next_fringe = []
        
        itter_cnt += 1

        # Expand each item in the fringe
        
        processes = []
        
        found_goals = []
        
        # MULTIPROCESSING
        # for _, state in fringe:
        #     process = pool.apply_async(func=expand_linker_search_state, args=(problem, state, max_children_per_expansion))
        #     processes.append(process)
        
        # for process in processes:
        #     goal, children = process.get()
        #     if goal is not None:
        #         found_goals.append(goal)
        #         continue
        #     for child in children:
        #         heapq.heappush(next_fringe, child)
        
        # SINGLE CORE
        for _, state in fringe:
            goal, children = expand_linker_search_state(problem, state, max_children_per_expansion)
            if goal is not None:
                found_goals.append(goal)
                continue
            for child in children:
                heapq.heappush(next_fringe, child)
        
        # If any goals were found, return the best one
        if len(found_goals) > 0:
            best_goal = found_goals[0]
            for goal in found_goals:
                if goal.cost_to_state < best_goal.cost_to_state:
                    best_goal = goal
            return best_goal.path
        
        # Enforce beam limit
        visited_this_search_level = set()
        fringe = []
        while len(next_fringe) > 0 and len(fringe) < beam_width:
            fringe_item = heapq.heappop(next_fringe)
            if fringe_item in visited_this_search_level:
                continue
            heapq.heappush(fringe, fringe_item)
            visited_this_search_level.add(fringe_item)
            
        dump_linker_open_list(problem, fringe, itter_cnt)

        pbar.update()
        
        # Failed to find goal
        if len(fringe) == 0:
            break
    
    raise Exception("Linker Failed To Find Path")


def get_linked_path(layers):
    
    total_image_mask = layers[0][0].get_entity_grid_mask().copy()
    for layer in layers:
        for entity in layer:
            total_image_mask = get_numpy_grid_mask_union(total_image_mask, entity.get_entity_grid_mask())
    
    problem = LinkerProblem(
        layers=layers,
        total_image_mask=total_image_mask,
        cost_menu=CostMenu(
            visited_mask_cost=10000,
            future_mask_cost=1,
            base_cost=10,
        )
    )
    
    return get_single_linked_path(problem, max_children_per_expansion=4, beam_width=2, heuristic_weight=2)
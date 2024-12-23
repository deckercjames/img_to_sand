
from src.linker.linkable_entity.linkable_entity import LinkableEntity
from typing import List, Set
from src.utils import get_neighbor_points
from src.utils import check_grid_element_safe
from src.utils import check_numpy_grid_element_safe
from src.utils import get_grid_mask_union
import heapq
from copy import deepcopy
from src.linker.linkable_entity.linkable_entity import EntityReference
import sys
from src.linker.linker_problem import *
import numpy as np
import numpy.typing as npt

from dataclasses import dataclass

ROOT_TWO = 1.414


@dataclass
class GetChildrenProblem:
    layers: List[List[LinkableEntity]]
    start_entity_ref: EntityReference
    search_layer_idx: int
    search_entity_refs: Set[EntityReference]
    child_visited_entity_ref_set: Set[EntityReference]
    visited_mask: npt.NDArray
    linker_path: List[PathItem]
    cost_to_linker_state: float
    cost_map: npt.NDArray
    def get_num_rows(self):
        return self.cost_map.shape[0] - 1
    def get_num_cols(self):
        return self.cost_map.shape[1] - 1
    

@dataclass
class GetChildrenSearchState:
    position: tuple[int, int]
    path: List[tuple[int, int]]
    cost: float
    def __lt__(self, other):
        return True


def _print_fringe(problem: GetChildrenProblem, fringe):
    # print(problem.num_rows, problem.num_cols)
    grid = [[' ' for _ in range(problem.get_num_cols() + 1)] for _ in range(problem.get_num_rows() + 1)]
    print(fringe[0])
    for e_ref in problem.search_entity_refs:
        for r,c in problem.layers[e_ref.layer_idx][e_ref.entity_idx].get_entry_points():
            grid[r][c] = '$'
    for i, s in enumerate(fringe):
        r,c = s[1].position
        grid[r][c] = '#'
    r,c = fringe[0][1].position
    grid[r][c] = '*'
    buf = ""
    buf += "+" + ("-" * len(grid[0])) + "+\n"
    for row in grid:
        buf += '|'
        for cel in row:
            buf += cel
        buf += "|\n"
    buf += "+" + ("-" * len(grid[0])) + "+\n"
    print(buf)
    print(len(fringe))
    print([s.position for _,s in fringe])


def check_reached_new_entity(problem: GetChildrenProblem, state: GetChildrenSearchState) -> EntityReference:
    
    r, c = state.position
    
    for entity_ref in problem.search_entity_refs:
        entity = problem.layers[entity_ref.layer_idx][entity_ref.entity_idx]
        if entity.is_location_an_entry_point(r, c):
            return entity_ref
    
    return None


def check_reached_border(problem: GetChildrenProblem, state: GetChildrenSearchState) -> bool:
    r,c = state.position
    return r == 0 or r == problem.get_num_rows() or c == 0 or c == problem.get_num_cols()


def get_border_heuristic(problem: GetChildrenProblem, state: GetChildrenSearchState) -> float:
    r,c = state.position
    dists = [
        r, c,
        problem.get_num_rows() - r + 1,
        problem.get_num_cols() - c + 1,
    ]
    return min(dists)


def get_heuristic(problem: GetChildrenProblem, state: GetChildrenSearchState, can_find_border: bool) -> float:
    
    best_dist = sys.float_info.max
    
    r, c = state.position
    
    for entity_ref in problem.search_entity_refs:
        entity = problem.layers[entity_ref.layer_idx][entity_ref.entity_idx]
        min_r, min_c, max_r, max_c = entity.get_bounding_box()
        # Check where r,c are in relation to the bounding box
        dr = 0 if (r >= min_r and r <= max_r) else ((min_r - r) if r < min_r else (r - max_r))
        dc = 0 if (c >= min_c and c <= max_c) else ((min_c - c) if c < min_c else (c - max_c))
        # We are withing the bounding box of any entity we are searching for
        if dr == 0 and dc == 0:
            return 0
        dist = min(dr, dc) * ROOT_TWO + (max(dr, dc) - min(dr, dc))
        best_dist = min(best_dist, dist)
    
    if can_find_border:
        border_dist = get_border_heuristic(problem, state)
        best_dist = min(best_dist, border_dist)
    
    return best_dist


def generate_child_state(problem: GetChildrenProblem, current_state: GetChildrenSearchState, child_entity_ref: EntityReference, child_linkage_points, child_cost: float):
    child_visited_entity_ref_set = problem.child_visited_entity_ref_set.copy()
    if child_entity_ref.entity_idx is not None:
        child_visited_entity_ref_set.add(child_entity_ref)
        child_visited_mask = np.logical_or(problem.visited_mask, problem.layers[child_entity_ref.layer_idx][child_entity_ref.entity_idx].get_entity_grid_mask())
    else:
        child_visited_mask = problem.visited_mask.copy()
    child = LinkerSearchState(
        cur_entity_ref=child_entity_ref,
        visited_mask=child_visited_mask,
        visited_entity_ref_set=child_visited_entity_ref_set,
        cost_to_state=problem.cost_to_linker_state+child_cost,
        path=problem.linker_path.copy() + [PathItem(child_linkage_points, child_entity_ref)]
    )
    return child


def search_for_close_entity_links(problem: GetChildrenProblem, num_children: int):
    
    child_states = []
    
    # print("HERE")
    # print("border_is_goal "+str(border_is_goal))
    # print(problem.start_entity_ref)
    start_points = set()
    if problem.start_entity_ref.entity_idx is None: # Start on the boarder
        for r in range(problem.get_num_rows()):
            start_points.add((r,0))
            start_points.add((r,problem.get_num_cols()))
        for c in range(problem.get_num_cols()):
            start_points.add((0, c))
            start_points.add((problem.get_num_rows(), c))
        start_points.add((problem.get_num_rows(), problem.get_num_cols()))
    else: # start at an entity
        start_points = problem.layers[problem.start_entity_ref.layer_idx][problem.start_entity_ref.entity_idx].get_exit_points()
    
    fringe = []
    
    can_find_border = problem.start_entity_ref.entity_idx is not None
    
    # Add all exit points from the current entity
    for start_point in start_points:
        start_state = GetChildrenSearchState(
            position=start_point,
            path=[start_point],
            cost=0
        )
        h = get_heuristic(problem, start_state, can_find_border)
        heapq.heappush(fringe, (h, start_state))

    # TODO handle inconsistant heuristic
    visited = set()
    
    while len(fringe) > 0:
        
        # _print_fringe(problem, fringe)
        
        _, cur_state = heapq.heappop(fringe)
        
        if cur_state.position in visited:
            continue
        
        # check if this is a goal state
        child_state_added = False
        # if border_is_goal:
        if can_find_border and check_reached_border(problem, cur_state):
            child_states.append(generate_child_state(problem, cur_state, EntityReference(problem.search_layer_idx, None), cur_state.path, cur_state.cost))
            child_state_added = True
            can_find_border = False
        # else:
        reached_entity_ref = check_reached_new_entity(problem, cur_state)
        if reached_entity_ref is not None:
            child_states.append(generate_child_state(problem, cur_state, reached_entity_ref, cur_state.path, cur_state.cost))
            problem.search_entity_refs.remove(reached_entity_ref)
            child_state_added = True

        if len(child_states) == num_children:
            return child_states
        
        if len(problem.search_entity_refs) == 0 and not can_find_border:
            return child_states

        # Reorder fringe based on changed heuristic
        if child_state_added:
            new_fringe = []
            while len(fringe) > 0:
                _, node = heapq.heappop(fringe)
                heuristic = get_heuristic(problem, node, can_find_border)
                heapq.heappush(new_fringe, (heuristic + node.cost, node))
            fringe = new_fringe

        # Mark as visited
        visited.add(cur_state.position)
        
        # expand the current state
        r, c = cur_state.position
        for nr, nc in get_neighbor_points(r, c):
            # Check on board
            if nr < 0 or nr >= problem.cost_map.shape[0] or nc < 0 or nc >= problem.cost_map.shape[1]:
                continue
            # Check visited
            if (nr, nc) in visited:
                continue
            # Add to fringe
            new_path = cur_state.path.copy()
            new_path.append((nr, nc))
            step_cost = check_numpy_grid_element_safe(problem.cost_map, r, c, default=0)
            if nr != r and nc != c:
                step_cost *= ROOT_TWO
            new_cost = cur_state.cost + step_cost
            child = GetChildrenSearchState(
                position=(nr, nc),
                path=new_path,
                cost=new_cost
            )
            heuristic = get_heuristic(problem, child, can_find_border)
            heapq.heappush(fringe, (new_cost + heuristic, child))
            
    raise Exception("Failed to get child state")


def _get_search_entity_refs(problem: LinkerProblem, current_state: LinkerSearchState):
    
    # print("CurrentState {")
    # print("  current_entity_ref: {}".format(str(current_state.cur_entity_ref)))
    # print("  visited_layer_entity_idx_set: {}".format(str(current_state.visited_layer_entity_idx_set)))
    # print("  ...\n}")
    
    search_set = set()
    
    # Get all unvisited entities in the current layer
    current_layer = current_state.cur_entity_ref.layer_idx
    for entity_idx in range(len(problem.layers[current_layer])):
        if EntityReference(current_layer, entity_idx) in current_state.visited_entity_ref_set:
            continue
        search_set.add(EntityReference(current_layer, entity_idx))
        
    # print(str(search_set))
    
    if len(search_set) > 0:
        return current_layer, search_set
    
    # If there were no unvisited entities in the current layer, get all entities in the next layer
    next_layer = current_layer + 1
    
    # print("next layer idx: {}".format(next_layer))
    # print("number of layers: "+str(len(problem.layers)))
    
    if next_layer >= len(problem.layers):
        return set()
    
    return next_layer, {EntityReference(next_layer, i) for i in range(len(problem.layers[next_layer]))}


def _get_cost_map(problem: LinkerProblem, current_state: LinkerSearchState):
    
    cost_map = np.empty(shape=(problem.get_num_rows()+1, problem.get_num_cols()+1))
    
    # print(problem.num_rows, problem.num_cols)
    # print(len(problem.total_image_mask), len(problem.total_image_mask[0]))
    
    for r in range(len(cost_map)):
        for c in range(len(cost_map[r])):
            # print(r, c)
            if check_numpy_grid_element_safe(current_state.visited_mask, r, c, default=False):
                cost_map[r, c] = problem.cost_menu.visited_mask_cost
            elif check_numpy_grid_element_safe(problem.total_image_mask, r, c, default=False):
                cost_map[r, c] = problem.cost_menu.future_mask_cost
            else:
                cost_map[r, c] = problem.cost_menu.base_cost
    
    # Bleed higher costs inward to encourage paths to stay away from the edges
    # for _ in range(5):
    #     new_cost_map = [[0 for _ in range(problem.num_cols)] for _ in range(problem.num_rows)]
    #     for r in range(problem.num_rows):
    #         for c in range(problem.num_cols):
    #             # print(r, c, type(cost_map))
    #             max_neighbor = max([check_grid_element_safe(cost_map, nr, nc, default=0) for nr, nc in get_neighbor_points(r,c)])
    #             if cost_map[r][c] >= max_neighbor:
    #                 new_cost_map[r][c] = cost_map[r][c]
    #                 continue
    #             new_cost_map[r][c] = cost_map[r][c] + (0.4 * (max_neighbor - cost_map[r][c]))
    #     cost_map = new_cost_map
    
    return cost_map


def get_child_states(problem: LinkerProblem, current_state: LinkerSearchState, num_children: int) -> List[LinkerSearchState]:
    
    # Set up the sub problem
    search_layer_idx, search_entity_refs = _get_search_entity_refs(problem, current_state)
    if len(search_entity_refs) == 0:
        raise Exception("No entities to search")
    
    sub_problem = GetChildrenProblem(
        layers=problem.layers,
        start_entity_ref=current_state.cur_entity_ref,
        search_layer_idx=search_layer_idx,
        search_entity_refs=search_entity_refs,
        child_visited_entity_ref_set=current_state.visited_entity_ref_set,
        visited_mask=current_state.visited_mask,
        linker_path=current_state.path,
        cost_to_linker_state=current_state.cost_to_state,
        cost_map=_get_cost_map(problem, current_state),
    )
    
    return search_for_close_entity_links(sub_problem, num_children)
    
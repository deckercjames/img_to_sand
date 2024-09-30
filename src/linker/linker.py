
from src.linker.layer_stratagem import get_all_layer_stratagem
from collections import namedtuple
from src.utils import get_all_false_mask
import heapq
from typing import List, Set
from copy import deepcopy
from dataclasses import dataclass
from src.utils import get_grid_mask_union
from src.linker.linkable_entity.linkable_entity import LinkableEntity
from src.utils import check_grid_element_safe

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
    num_rows: int
    num_cols: int
    cost_menu: CostMenu
    

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

entity_link_cache = {}


def get_all_points_along_line(p0: tuple[int, int], p1: tuple[int, int]) -> List[tuple[int, int]]:
    
    points = []
    
    r0, c0 = p0
    r1, c1 = p1

    dr = abs(r0 - r1)
    sr = 1 if r0 < r1 else -1
    dc = -abs(c0 - c1)
    sc = 1 if c0 < c1 else -1
    error = dr + dc
    
    while True:
        points.append((r0, c0))
        if r0 == r1 and c0 == c1:
            break
        e2 = 2 * error
        if e2 >= dc:
            if r0 == r1:
                break
            error = error + dc
            r0 = r0 + sr
        if e2 <= dr:
            if c0 == c1:
                break
            error = error + dr
            c0 = c0 + sc
    
    return points


def calculate_cost(problem: LinkerProblem, state: LinkerSearchState, p0: tuple[int, int], p1: tuple[int, int]) -> int:
    
    total_cost = 0
    
    # get all points along line
    for r,c in get_all_points_along_line(p0, p1):
        # Check if point is in no-go zone (goes over an entity already drawn)
        if check_grid_element_safe(state.visited_mask, r, c, default=False):
            total_cost += problem.cost_menu.visited_mask_cost
        elif check_grid_element_safe(problem.total_image_mask, r, c, default=False):
            total_cost += problem.cost_menu.future_mask_cost
        else:
            total_cost += problem.cost_menu.base_cost
    
    return total_cost


def get_entity_link_with_border(problem: LinkerProblem, connection_points: List[tuple[int, int]]) -> tuple[float, tuple[int, int], tuple[int, int]]:
    """
    Returns:
        (entity_point, border_point)
    """
    northern_most_pt = None
    southern_most_pt = None
    eastern_most_pt = None
    western_most_pt = None
    
    for point in connection_points:
        r, c = point
        if northern_most_pt is None or r < northern_most_pt[0]:
            northern_most_pt = point
        if southern_most_pt is None or r > southern_most_pt[0]:
            southern_most_pt = point
        if eastern_most_pt is None or c < eastern_most_pt[1]:
            eastern_most_pt = point
        if western_most_pt is None or c > western_most_pt[1]:
            western_most_pt = point


    possible_ret_values = []
    
    if northern_most_pt is not None:
        northern_point_border_point = (0, northern_most_pt[1])
        northern_point_cost = northern_most_pt[0]
        possible_ret_values.append((northern_point_cost, northern_most_pt, northern_point_border_point))
    
    if southern_most_pt is not None:
        southern_point_border_point = (problem.num_rows, southern_most_pt[1])
        southern_point_cost = problem.num_rows - southern_most_pt[0]
        possible_ret_values.append((southern_point_cost, southern_most_pt, southern_point_border_point))
    
    if eastern_most_pt is not None:
        eastern_point_border_point = (eastern_most_pt[0], 0)
        eastern_point_cost = eastern_most_pt[1]
        possible_ret_values.append((eastern_point_cost, eastern_most_pt, eastern_point_border_point))
    
    if western_most_pt is not None:
        western_point_border_point = (western_most_pt[0], problem.num_cols)
        western_point_cost = problem.num_cols - western_most_pt[1]
        possible_ret_values.append((western_point_cost, western_most_pt, western_point_border_point))

    best_cost = None
    best_idx = None
    for i, (cost, _, _) in enumerate(possible_ret_values):
        if best_idx is None or cost < best_cost:
            best_cost = cost
            best_idx = i
    
    for p in possible_ret_values:
        print(p)
    print("best idx"+str(best_idx))
    
    return (possible_ret_values[best_idx][1], possible_ret_values[best_idx][2])


def get_entity_link(problem: LinkerProblem, e0_ref: EntityReference, e1_ref: EntityReference) -> tuple[tuple[int, int], tuple[int, int]]:

    # First check cache
    cache_key = (e0_ref, e1_ref)
    if cache_key in entity_link_cache:
        return entity_link_cache[cache_key]
    
    # If not in the cache, calculate and add it
    best_from_pt = None
    best_to_pt = None
    
    e0 = problem.layers[e0_ref.layer_idx].linkable_entities[e0_ref.entity_idx] if e0_ref is not None else None
    e1 = problem.layers[e1_ref.layer_idx].linkable_entities[e1_ref.entity_idx] if e1_ref is not None else None
    
    # Connect entity to border
    if e1 is None:
        best_from_pt, best_to_pt = get_entity_link_with_border(problem, e0.get_exit_points())
    
    # Connect border to entity
    elif e0 is None:
        best_to_pt, best_from_pt =  get_entity_link_with_border(problem, e1.get_entry_points())
    
    # Conect entity to entity
    else:
        best_mag_sqrd = None
        for r0, c0 in e0.get_exit_points():
            for r1, c1 in e1.get_entry_points():
                mag_squared = (abs(r0 - r1) ** 2) + (abs(c0 - c1) ** 2)
                if best_mag_sqrd is None or mag_squared < best_mag_sqrd:
                    best_mag_sqrd = mag_squared
                    best_from_pt = (r0, c0)
                    best_to_pt = (r1, c1)
    
    # Add to cache and return
    ret = (best_from_pt, best_to_pt)
    entity_link_cache[cache_key] = ret
    return ret


def is_goal_state(problem: LinkerProblem, search_state) -> bool:
    cur_entity_ref = search_state.cur_entity_ref
    return cur_entity_ref.layer_idx == len(problem.layers) - 1 and cur_entity_ref.entity_idx == len(problem.layers.linkable_entities) - 1


def get_child_states(problem: LinkerProblem, current_state: LinkerSearchState) -> List[LinkerSearchState]:
    
    next_layer_idx = current_state.cur_entity_ref.layer_idx
    next_visited_layer_entity_idx_set = current_state.visited_layer_entity_idx_set
    
    # Check if this layer is complete
    if len(current_state.visited_layer_entity_idx_set) == len(problem.layers[current_state.cur_entity_ref.layer_idx].linkable_entities):
        # Move to next layer
        next_layer_idx += 1
        next_visited_layer_entity_idx_set = set()
    
    child_states = []
        
    # For every unvisited entity in the next layer (next layer could be the current layer)
    for linkable_entity_idx, linkable_entity in enumerate(problem.layers[next_layer_idx].linkable_entities):
        # If visited, ignore
        if linkable_entity_idx in current_state.visited_layer_entity_idx_set:
            continue
        # Set the entity reference
        child_entity_ref = EntityReference(next_layer_idx, linkable_entity_idx)
        # Update the visited set for this child
        child_visited_layer_entity_idx_set = next_visited_layer_entity_idx_set.copy()
        child_visited_layer_entity_idx_set.add(linkable_entity_idx)
        # Get the path item and the cost
        from_pt, to_pt = get_entity_link(problem, current_state.cur_entity_ref, linkable_entity)
        link_cost = calculate_cost(problem, from_pt, to_pt)
        # Child Path
        child_path = current_state.path.copy()
        child_path.append(PathItem(from_pt, child_entity_ref, to_pt))
        # Add child state to children
        child_state = LinkerSearchState(
            child_entity_ref,
            get_grid_mask_union(current_state.visited_mask, linkable_entity.get_entity_grid_mask()),
            child_visited_layer_entity_idx_set,
            current_state.cost_to_state + link_cost,
            child_path
        )
        child_states.append(child_state)
    
    # Special Case if the current state is not on the border, add a link to the boarder
    if current_state.cur_entity_ref is not None:
        from_pt, to_pt = get_entity_link(problem, current_state.cur_entity_ref, None)
        link_cost = calculate_cost(problem, from_pt, to_pt)
        child_path.append(PathItem(from_pt, None, to_pt))
        child_state = LinkerSearchState(
            None,
            current_state.visited_mask, # no change to the visited mask
            current_state.visited_layer_entity_idx_set, # no change to the visited entity set
            current_state.cost_to_state + link_cost,
            child_path
        )
        child_states.append(child_state)
    
    return child_states


def get_heuristic_for_state(layers, state):
    pass


def get_linked_path(problem: LinkerProblem):
    
    start_state = LinkerSearchState(
        None,
        get_all_false_mask(problem.num_rows, problem.num_cols),
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
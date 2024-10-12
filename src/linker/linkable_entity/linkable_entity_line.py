
from src.linker.linkable_entity.linkable_entity import LinkableEntity
from src.utils import check_grid_element_safe
from src.zhang_suen import _get_neighbours
from typing import List
from collections import deque


class LinkableEntityLine(LinkableEntity):
    def __init__(self, line_grid_mask, gateway_points):
        super().__init__(gateway_points)
        self.line_grid_mask = line_grid_mask
        self.gateway_points = gateway_points

    def get_entry_points(self):
        return self.gateway_points

    def get_exit_points(self):
        return self.gateway_points
        
    def get_entity_grid_mask(self):
        return self.line_grid_mask


def get_line_end_points(line_grid_mask):
    end_points = []
    # find all points that have only one neighbor
    for r in range(len(line_grid_mask)):
        for c in range(len(line_grid_mask[r])):
            if not line_grid_mask[r][c]:
                continue
            neighbors = _get_neighbours(line_grid_mask, r, c)
            neighbor_cnt = sum([1 if n else 0 for n in neighbors])
            if neighbor_cnt != 1:
                continue
            end_points.append((r, c))
    
    return end_points


def _get_point_on_mask(line_grid_mask):
    # Find a point in the grid mask
    for r in range(len(line_grid_mask)):
        for c in range(len(line_grid_mask[r])):
            if line_grid_mask[r][c]:
                return (r,c)
            
    raise Exception("Expected at least one cell set")


def get_equally_spaced_gateway_points(line_grid_mask, spacing):
    fringe = deque()
    fringe.append(None)
    fringe.append(_get_point_on_mask(line_grid_mask))
    # Use a None marker to represent one full pass througth the queue
    # Every 'spacing' passes through the queue, add the entire fringe to the list
    
    visited = set()
    gateway_points = []
    
    itter_cnt = 0
    
    # flood fill, caching the fringe points
    while len(fringe) > 1:
        # Append fringe to gateway points at regular intervals
        item = fringe.popleft()
        if item is None:
            if itter_cnt % spacing == 0:
                gateway_points.extend(fringe)
            itter_cnt += 1
            fringe.append(None)
            continue
        (r,c) = item
        visited.add((r,c))
        # Expand in all eight directions
        for nr, nc in [(r-1,c), (r-1,c+1), (r,c+1), (r+1,c+1), (r+1,c), (r+1,c-1), (r,c-1), (r-1,c-1)]:
            if not check_grid_element_safe(line_grid_mask, nr, nc):
                continue
            if (nr, nc) in visited:
                continue
            fringe.append((nr,nc))
        
    return gateway_points
        
    

def get_line_linkable_entity(line_grid_mask: List[List[bool]], spacing):
    gateway_points = get_line_end_points(line_grid_mask)
    if len(gateway_points) == 0:
        if spacing <= 0:
            raise Exception("Spacing must be a positive integer!")
        gateway_points = get_equally_spaced_gateway_points(line_grid_mask, spacing)
    return LinkableEntityLine(line_grid_mask, gateway_points)

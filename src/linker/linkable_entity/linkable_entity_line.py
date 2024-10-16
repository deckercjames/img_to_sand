
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


def get_all_points(line_grid_mask):
    
    all_points = []
    
    for r in range(len(line_grid_mask)):
        for c in range(len(line_grid_mask[r])):
            if line_grid_mask[r][c]:
                all_points.append((r,c))
        
    return all_points


def get_line_linkable_entity(line_grid_mask: List[List[bool]]):
    gateway_points = get_line_end_points(line_grid_mask)
    if len(gateway_points) == 0:
        gateway_points = get_all_points(line_grid_mask)
    return LinkableEntityLine(line_grid_mask, gateway_points)

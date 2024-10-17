
from abc import ABC, abstractmethod
from collections import namedtuple
from collections import namedtuple


BoundingBox = namedtuple("BoundingBox", ["r0", "c0", "r1", "c1"])

EntityReference = namedtuple("EntityReference", ["layer_idx", "entity_idx"])

class LinkableEntity(ABC):
    def __init__(self, entry_points):
        self.entry_points_set = set(entry_points)
        self._calculate_bounding_box()
        
    def _calculate_bounding_box(self):
        for r, c in self.entry_points_set:
            min_r = r
            min_c = c
            max_r = r
            max_c = c
            break
        for r, c in self.entry_points_set:
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)
        self.bounding_box = BoundingBox(min_r, min_c, max_r, max_c)
        
    def is_location_an_entry_point(self, r, c):
        return (r,c) in self.entry_points_set
    
    def get_bounding_box(self):
        return self.bounding_box
    
    @abstractmethod
    def get_entry_points(self, spacing):
        pass

    @abstractmethod
    def get_exit_points(self, spacing):
        pass
    
    @abstractmethod
    def get_entity_grid_mask(self):
        pass


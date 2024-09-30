
from abc import ABC, abstractmethod
from collections import namedtuple
from enum import Enum
from typing import List


class LinkableEntity(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def get_entry_points(self, spacing):
        pass

    @abstractmethod
    def get_exit_points(self, spacing):
        pass
        
    def get_entity_grid_mask(self):
        return self.blob.mask


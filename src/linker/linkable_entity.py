
from abc import ABC, abstractmethod
from collections import namedtuple
from enum import Enum


class LinkableEntity(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def get_entry_points(self):
        pass

    @abstractmethod
    def get_exit_points(self):
        pass
        
    @abstractmethod
    def get_entity_grid_mask(self):
        pass


class LinkableEntityLine(LinkableEntity):
    def __init__(self, line_grid_mask):
        super.__init__()
        self.line_grid_mask = line_grid_mask


class LinkableEntityBlob(LinkableEntity):
    def __init__(self, blob):
        super.__init__()
        self.blob = blob


def get_line_linkable_entity(line_blob):
    pass

def get_blob_linkable_entity(blob):
    pass
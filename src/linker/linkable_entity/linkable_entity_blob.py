

from src.linker.linkable_entity.linkable_entity import LinkableEntity
from src.blob_extraction import Blob
from src.topography import get_blob_topography
from src.topography import get_topography_tree_visual
from src.tree import TreeNode

class LinkableEntityBlob(LinkableEntity):
    def __init__(self, blob, entry_points, exit_points):
        self.blob = blob
        self.entry_points = entry_points
        self.exit_point = exit_points

    def get_entry_points(self):
        return self.entry_points

    def get_exit_points(self):
        return self.exit_point



def get_leaf_entry_points(blob_topography: TreeNode, spacing: int):
    
    if len(blob_topography.children) == 0:
        return blob_topography.node_data[::spacing]
    
    leaf_entry_points = []
    
    for child in blob_topography.children:
        leaf_entry_points.extend(get_leaf_entry_points(child, spacing))
    
    return leaf_entry_points
    


def get_blob_linkable_entity(blob: Blob, spacing: int):
    exit_points = blob.outer_contour[::spacing]
    blob_topograph = get_blob_topography(blob)
    print(get_topography_tree_visual(blob_topograph, len(blob.mask), len(blob.mask[0])))
    entry_points = get_leaf_entry_points(blob_topograph, spacing)
    return LinkableEntityBlob(blob, entry_points, exit_points)
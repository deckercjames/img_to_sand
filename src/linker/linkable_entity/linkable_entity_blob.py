

from src.linker.linkable_entity.linkable_entity import LinkableEntity
from src.image_parsing.blob_extraction import Blob
from src.linker.linkable_entity.topography import get_blob_topography
from src.linker.linkable_entity.topography import get_topography_tree_visual
from src.tree import TreeNode

class LinkableEntityBlob(LinkableEntity):
    def __init__(self, blob: Blob, blob_topography: TreeNode, entry_points, exit_points):
        super().__init__(entry_points)
        self.blob = blob
        self.blob_topography = blob_topography
        self.entry_points = entry_points
        self.exit_point = exit_points

    def get_entry_points(self):
        return self.entry_points

    def get_exit_points(self):
        return self.exit_point

    def get_entity_grid_mask(self):
        return self.blob.mask




def get_leaf_entry_points(blob_topography: TreeNode):
    
    if len(blob_topography.children) == 0:
        return blob_topography.node_data
    
    leaf_entry_points = []
    
    for child in blob_topography.children:
        leaf_entry_points.extend(get_leaf_entry_points(child))
    
    return leaf_entry_points
    


def get_blob_linkable_entity(blob: Blob):
    exit_points = blob.outer_contour
    blob_topography = get_blob_topography(blob)
    # print(get_topography_tree_visual(blob_topography, len(blob.mask), len(blob.mask[0])))
    entry_points = get_leaf_entry_points(blob_topography)
    if blob_topography.children != 0:
        entry_points.extend(blob_topography.node_data)
    return LinkableEntityBlob(blob, blob_topography, entry_points, exit_points)
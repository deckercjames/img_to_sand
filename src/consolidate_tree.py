
from src.tree import TreeNode
from src.utils import grid_mask_union
from src.utils import get_all_false_mask

from collections import namedtuple


ConsolidatedTreeData = namedtuple("ConsolidatedTreeData", ["parental_mask_union", "blobs"])


def _consolidate_blob_tree(root, parental_mask_union):

    if len(root.children) == 0:
        return None
    
    parental_and_self_mask_union = parental_mask_union
    if root.node_data is not None:
        parental_and_self_mask_union = grid_mask_union(parental_mask_union, root.node_data.mask)
    
    consolidated_tree_root = TreeNode(ConsolidatedTreeData(parental_and_self_mask_union, []), children=[])

    for child in root.children:
        consolidated_tree_root.node_data.blobs.append(child.node_data)
        consolidated_child = _consolidate_blob_tree(child, parental_and_self_mask_union)
        if consolidated_child is not None:
            consolidated_tree_root.children.append(consolidated_child)

    return consolidated_tree_root
        


def consolidate_blob_trees(blob_trees, num_rows, num_cols):
    
    # Starting mask is all False
    starting_mask = get_all_false_mask(num_rows, num_cols)
    
    # Assign all blob trees to a single phantom root so the algorithm is easier
    phantom_root = TreeNode(None, children=blob_trees)
    
    return _consolidate_blob_tree(phantom_root, starting_mask)
    
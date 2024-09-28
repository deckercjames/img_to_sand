
from src.tree import TreeNode


def _consolidate_blob_tree(root):

    if len(root.children) == 0:
        return None
    
    consolidated_tree_root = TreeNode([], children=[])

    for child in root.children:
        consolidated_tree_root.node_data.append(child.node_data)
        consolidated_child = _consolidate_blob_tree(child)
        if consolidated_child is not None:
            consolidated_tree_root.children.append(consolidated_child)

    return consolidated_tree_root
        


def consolidate_blob_trees(blob_trees, num_rows, num_cols):

    # Assign all blob trees to a single phantom root so the algorithm is easier
    phantom_root = TreeNode(None, children=blob_trees)
    
    return _consolidate_blob_tree(phantom_root)
    

from src.linker.linkable_entity.linkable_entity_blob import LinkableEntityBlob
from dataclasses import dataclass
from src.tree import TreeNode
from typing import List, Set, Final
from src.utils import get_cyclic_list_slice
from src.utils import get_list_element_cyclic


@dataclass
class ElaboratorTreeNode:
    contour: List[tuple[int, int]]
    elaborated: bool
    parent: 'ElaboratorTreeNode'
    children: List['ElaboratorTreeNode']


def convert_topography_to_elaborator_tree(blob_topography_node: TreeNode, parent: ElaboratorTreeNode=None):
    
    new_node = ElaboratorTreeNode(
        contour=blob_topography_node.node_data,
        elaborated=False,
        parent=parent,
        children=[]
    )
    
    for blob_topography_child_node in blob_topography_node.children:
        new_child = convert_topography_to_elaborator_tree(blob_topography_child_node, parent=new_node)
        new_node.children.append(new_child)
    
    return new_node


def find_entry_node(node: ElaboratorTreeNode, entry_point: tuple[int, int]):
    
    # The entry node is gaurenteed to be on the root or a leaf
    if node.parent is None or len(node.children) == 0:
        if entry_point in node.contour:
            return node
    
    # recurse on all children
    for child in node.children:
        result = find_entry_node(child, entry_point)
        if result is None:
            continue
        return result
    
    raise Exception("Could not find entry node")
    

def link_adjacent_contours(current_contour, next_contour, start_contour_idx):
    """
    The contours must be orthagonally adjacent at some point
    """
    next_contour_map = {point:i for i, point in enumerate(next_contour)}
    
    link_path = []
    
    for i in range(len(current_contour)):
        
        current_contour_idx = (start_contour_idx + i) % len(current_contour)
        
        link_path.append(current_contour[current_contour_idx])
        
        # check if current point on the current contour can link with the next one
        r, c = current_contour[current_contour_idx]
        orth_neighbors = ((r+1,c), (r-1,c), (r,c+1), (r,c-1))
        
        for neighbor in orth_neighbors:
            if neighbor not in next_contour_map:
                continue
            link_path.append(neighbor)
            return link_path, next_contour_map[neighbor]
        
    raise Exception("Could not find link between contours")


def elaborate_blob(entity: LinkableEntityBlob, entry_point: tuple[int, int], exit_point: tuple[int, int], spiral_spacing: int):
    
    elaborator_tree_root = convert_topography_to_elaborator_tree(entity.blob_topography)
    
    entry_node = find_entry_node(elaborator_tree_root, entry_point)
    
    elaboration_contour_fraction: Final[float] = 1 / spiral_spacing

    # Now we actually elaborate the node
    current_node: ElaboratorTreeNode = entry_node
    current_contour_idx = current_node.contour.index(entry_point)
    path = [entry_point]
    
    itter_cnt = 0
    
    while True:
        
        # First, elaborate any child that has not been elaborated yet
        traverse_to_child = None
        for child in current_node.children:
            if child.elaborated:
                continue
            traverse_to_child = child
            break
        
        # If there is an un-elaborated child, move there
        if traverse_to_child is not None:
            inter_contour_path, current_contour_idx = link_adjacent_contours(current_node.contour, traverse_to_child.contour, current_contour_idx)
            path.extend(inter_contour_path)
            current_node = traverse_to_child
            continue
        
        # elaborate the current node, now that all children have been taken care of
        if len(current_node.children) == 0 or current_node.parent is None:
            elaborated_segment_length = len(current_node.contour)
        else:
            elaborated_segment_length = int(len(current_node.contour) * elaboration_contour_fraction)
        
        next_contour_index = (current_contour_idx + elaborated_segment_length) % len(current_node.contour)
        path.extend(get_cyclic_list_slice(current_node.contour, current_contour_idx, next_contour_index))
        current_node.elaborated = True
        
        # If there is no parent, we are done
        if current_node.parent is None:
            break
        
        # Traverse up the tree to the parent
        inter_contour_path, current_contour_idx = link_adjacent_contours(current_node.contour, current_node.parent.contour, next_contour_index)
        path.extend(inter_contour_path)
        current_node = current_node.parent
    
    # Traverse to exit point if provided
    if exit_point is not None:
        for i in range(len(current_node.contour)):
            check_point = get_list_element_cyclic(current_node.contour, current_contour_idx+i)
            path.append(check_point)
            if check_point == exit_point:
                break
        else:
            raise Exception("Could not find exit point ({},{})".format(*exit_point))
        
    return path


from src.utils import check_grid_element_safe
from src.blob_extraction import get_blob_mask_outer_contour
from src.blob_extraction import get_total_blob_mask
from src.zhang_suen import zhang_suen_errosion_itteration
from src.blob_extraction import Blob
from src.utils import get_grid_mask_subtraction
from src.utils import get_grid_mask_union
from src.utils import grid_mask_to_str
from src.utils import check_mask_intersection
from src.utils import get_list_element_cyclic
from src.utils import get_mask_with_inward_bleed
from copy import deepcopy
from collections import namedtuple
from src.tree import TreeNode


def _apply_topography_tree_node_to_visual_rep(node, hor_fences, vert_fences):
    
    contour = node.node_data
    
    # populate fence tables
    for i, point in enumerate(contour):
        r, c = point
        prev_r, prev_c = get_list_element_cyclic(contour, i - 1)
        if r == prev_r:
            hor_fences[r][min(c, prev_c)] = True
        elif c == prev_c:
            vert_fences[min(r, prev_r)][c] = True
        else:
            raise Exception("Somethiing has gone horribally wrong")
    
    # recurse on children
    for child in node.children:
        _apply_topography_tree_node_to_visual_rep(child, hor_fences, vert_fences)


def get_topography_tree_visual(root, num_rows, num_cols):
    
    # break the contour list into a grid of horizontal and vertical boundaries ("fences")
    hor_fences  = [[False for _ in range(num_cols)] for _ in range(num_rows + 1)]
    vert_fences = [[False for _ in range(num_cols + 1)] for _ in range(num_rows)]
    
    _apply_topography_tree_node_to_visual_rep(root, hor_fences, vert_fences)
    
    # convert polulated fences to string
    buf = ""
    for i in range(num_rows):
        # hor fences
        for c in range(num_cols):
            buf += "+"
            buf += '--' if hor_fences[i][c] else "  "
        buf += "+\n"
        # vert fences
        for c in range(num_cols + 1):
            buf += "|" if vert_fences[i][c] else " "
            if c != num_cols:
                buf += "  "
        buf += "\n"
    # last hor fence row
    for c in range(num_cols):
        buf += "+"
        buf += '--' if hor_fences[num_rows][c] else "  "
    buf += "+\n"
    return buf
    

def get_flood_fill_grid_mask(grid_mask, start_r, start_c, diag=False):
    cell_stack = []
    cell_stack.append((start_r, start_c))

    grid_blob_mask = [[False for _ in range(len(row))] for row in grid_mask]
    
    while len(cell_stack) > 0:
        r, c = cell_stack.pop()
        if r < 0 or r >= len(grid_mask) or c < 0 or c >= len(grid_mask[0]):
            continue
        # already visited
        if grid_blob_mask[r][c]:
            continue
        # check if pixel should be included
        if not grid_mask[r][c]:
            continue
        # expand pixel
        cell_stack.append((r + 1, c))
        cell_stack.append((r - 1, c))
        cell_stack.append((r, c - 1))
        cell_stack.append((r, c + 1))
        if diag:
            cell_stack.append((r + 1, c - 1))
            cell_stack.append((r + 1, c + 1))
            cell_stack.append((r - 1, c - 1))
            cell_stack.append((r - 1, c + 1))
        grid_blob_mask[r][c] = True
    
    return grid_blob_mask


def get_all_blobs_from_mask(grid_mask):
    """
    Gets all the contours of a grid mask with positive "blobs".
    This can be used for getting the contours of a void within a blob
    There can be no nested mask contours
    """
    blobs = []
    
    num_rows = len(grid_mask)
    num_cols = len(grid_mask[0])
    
    for r in range(num_rows):
        for c in range(num_cols):
            if not grid_mask[r][c]:
                continue
            grid_blob_mask = get_flood_fill_grid_mask(grid_mask, r, c)
            grid_blob_contour = get_blob_mask_outer_contour(grid_blob_mask, r, c)
            grid_blob_total_mask = get_total_blob_mask(grid_blob_contour, num_rows, num_cols)
            blob = Blob(grid_blob_contour, grid_blob_mask, grid_blob_total_mask)
            grid_mask = get_grid_mask_subtraction(grid_mask, grid_blob_mask)
            blobs.append(blob)
    
    return blobs


def decant_mask_data_from_topography_tree(tree_node):
    tree_node.node_data = tree_node.node_data.outer_contour
    for child in tree_node.children:
        decant_mask_data_from_topography_tree(child)


def get_blob_topography(blob: Blob) -> TreeNode:
    
    # Get the void regions
    root_node = TreeNode(blob, [])
    positive_branchs = [
        root_node
    ]
    
    root_voids_mask = get_grid_mask_subtraction(blob.total_mask, blob.mask)
    negative_branches = [TreeNode(b, []) for b in get_all_blobs_from_mask(root_voids_mask)]
    
    
    main_mask = blob.mask
    
    while True:
        # print("Num pos branches "+str(len(positive_branchs)))
        # print("Num neg branches "+str(len(negative_branches)))
        main_mask = get_mask_with_inward_bleed(main_mask, diag_bleed=True)
        # print("Current main mask")
        # print(grid_mask_to_str(main_mask))
        
        # grow tree in positive direction
        positive_blobs = get_all_blobs_from_mask(main_mask)
        positive_nodes = [TreeNode(b, []) for b in positive_blobs]
        
        # invert mask
        void_mask = [[False for _ in range(len(row))] for row in main_mask]
        for positive_blob in positive_blobs:
            void_mask = get_grid_mask_union(void_mask, positive_blob.total_mask)
        for positive_blob in positive_blobs:
            void_mask = get_grid_mask_subtraction(void_mask, positive_blob.mask)
        # print("Current main void mask")
        # print(grid_mask_to_str(void_mask))
        
        # get all new void nodes
        negative_blobs = get_all_blobs_from_mask(void_mask)
        new_negative_nodes = [TreeNode(b, []) for b in negative_blobs]
        # print("num new neg void nodes "+str(len(new_negative_nodes)))
        
        # assign new negative nodes to negative branches
        for new_negative_node in new_negative_nodes:
            # print("Assigning neg branches to negative node")
            # print(grid_mask_to_str(new_negative_node.node_data.mask))
            # check which negative branges it grows to (can be multiple)
            for i in range(len(negative_branches)-1, -1, -1):
                # print("Checking existing neg branch "+str(i))
                # print(grid_mask_to_str(negative_branches[i].node_data.mask))
                if not check_mask_intersection(new_negative_node.node_data.mask, negative_branches[i].node_data.mask):
                    continue
                # print("Found match for branch "+str(i))
                new_negative_node.children.append(negative_branches[i])
                del negative_branches[i]
        
        # print("Num unasigned negative nodes "+str(len(negative_branches)))
        
        # any unassigned negative branches join with the positive ones
        for negative_branch in negative_branches:
            # print("Attempting to assign negative branch to positive branch")
            # print(grid_mask_to_str(negative_branch.node_data.mask))
            # Check which positive branch it matches to
            for positive_branch in positive_branchs:
                # print("Comparing to positive branch")
                # print(grid_mask_to_str(positive_branch.node_data.total_mask))
                if not check_mask_intersection(negative_branch.node_data.mask, positive_branch.node_data.total_mask):
                    continue
                # print("Match found!")
                positive_branch.children.append(negative_branch)
                break
            else:
                raise Exception("All negative branches should have matched up with a positive one")
    
        # update the negative branch end cache to point at the new ends of the branches   
        negative_branches = new_negative_nodes
        
        # Break condition
        if len(positive_nodes) == 0:
            break
        
        # assign new positive nodes to positive branch ends
        for positive_node in positive_nodes:
            # check which positive branch end this node belongs to
            for positive_branch in positive_branchs:
                if not check_mask_intersection(positive_node.node_data.mask, positive_branch.node_data.mask):
                    continue
                positive_branch.children.append(positive_node)
                
        # assign cached positive branches to be the new ends
        positive_branchs = positive_nodes
    
    # the mask data was needed in the tree nodes to build the tree, but it does
    # not need to be returned
    decant_mask_data_from_topography_tree(root_node)
    
    return root_node


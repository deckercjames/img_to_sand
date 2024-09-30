
from src.linker.linker import get_child_states
from src.linker.linker import LinkerProblem
from src.linker.linker import CostMenu
from src.linker.linker import LinkerSearchState
from src.linker.linker import EntityReference
from src.utils import get_all_false_mask
from src.blob_extraction import get_blob_tree_nodes_from_pixel_grid
from src.consolidate_tree import consolidate_blob_trees
from src.tree import unwrap_tree_post_order_traversal
from src.linker.layer_stratagem import get_all_layer_stratagem

def helper_pixel_grid_str_parser(pixel_grid_str):
    pixel_grid = []
    for line in pixel_grid_str:
        pixel_grid.append(
            [0 if c == ' ' else int(c) for c in line]
        )
    return pixel_grid

def helper_get_layers(pixel_grid_str):
    pixel_grid = helper_pixel_grid_str_parser(pixel_grid_str)
    num_rows = len(pixel_grid)
    num_cols = len(pixel_grid[0])
    
    # Extract blobs
    blob_trees = get_blob_tree_nodes_from_pixel_grid(pixel_grid)
    
    # Consolidate blob trees
    consolidated_blob_tree = consolidate_blob_trees(blob_trees, num_rows, num_cols)
    
    # Unwrap consolidated blob tree
    blob_layers = unwrap_tree_post_order_traversal(consolidated_blob_tree)

    return get_all_layer_stratagem(blob_layers, num_line_errosion_itterations=0, num_blob_buffer_itterations=0, gateway_point_spacing=1)
    
    


def test_get_child_states_from_beginning():
    pixel_grid_str = [
        "                  ",
        "  11      222222  ",
        " 1111      22222  ",
        "   11     2222222 ",
        "                  ",
    ]
    layers = helper_get_layers(pixel_grid_str)
    print("LAYERS")
    print(layers)
    # build the layers with the other code. Assume it to be correct
    test_problem = LinkerProblem(
        layers=layers, # Not used by the tested function
        total_image_mask=[
            [False, True,  True,  True,  False]
        ],
        num_rows=5,
        num_cols=18,
        cost_menu=CostMenu(
            visited_mask_cost=100000,
            future_mask_cost=0,
            base_cost=1
        )
    )
    test_state = LinkerSearchState(
        cur_entity_ref=EntityReference(0, None), # Start at border
        visited_mask=get_all_false_mask(test_problem.num_rows, test_problem.num_cols),
        visited_layer_entity_idx_set=set(),
        cost_to_state=0,
        path=[]
    )
    recv_child_states = get_child_states(test_problem, test_state)
    exp_child_states = [
        LinkerSearchState(),
    ]
    assert recv_child_states == exp_child_states
    
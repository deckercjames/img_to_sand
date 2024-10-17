
from src.linker.linker import get_child_states
from src.linker.linker import LinkerProblem
from src.linker.linker import CostMenu
from src.linker.linker import LinkerSearchState
from src.linker.linker import PathItem
from src.linker.linker import EntityReference
from src.utils import get_all_false_mask
from src.utils import grid_mask_to_str
from src.blob_extraction import get_blob_tree_nodes_from_pixel_grid
from src.consolidate_tree import consolidate_blob_trees
from src.tree import unwrap_tree_post_order_traversal
from copy import deepcopy
from src.linker.layer_stratagem import get_all_layer_stratagem

def helper_pixel_grid_str_parser(pixel_grid_str):
    pixel_grid = []
    for line in pixel_grid_str:
        pixel_grid.append(
            [0 if c == ' ' else int(c) for c in line]
        )
    return pixel_grid


def helper_get_layers(pixel_grid_str, num_line_errosions=0):
    pixel_grid = helper_pixel_grid_str_parser(pixel_grid_str)
    num_rows = len(pixel_grid)
    num_cols = len(pixel_grid[0])
    
    # Extract blobs
    blob_trees = get_blob_tree_nodes_from_pixel_grid(pixel_grid)
    
    # Consolidate blob trees
    consolidated_blob_tree = consolidate_blob_trees(blob_trees, num_rows, num_cols)
    
    # Unwrap consolidated blob tree
    blob_layers = unwrap_tree_post_order_traversal(consolidated_blob_tree)
    
    layers = get_all_layer_stratagem(blob_layers, num_line_errosion_itterations=num_line_errosions, num_blob_buffer_itterations=0)
    
    total_image_mask = [[c != ' ' for c in line] for line in pixel_grid_str]

    return layers, total_image_mask
    

def helper_print_path_item(layers, path_item: PathItem):
    assert type(path_item) == PathItem
    num_rows = len(layers[0][0].get_entity_grid_mask())
    num_cols = len(layers[0][0].get_entity_grid_mask()[0])
    rep = [[' ' for _ in range(num_cols+1)] for _ in range(num_rows+1)]
    # apply entity
    entity_ref = path_item.next_entity_ref
    if entity_ref.entity_idx is not None:
        entity = layers[entity_ref.layer_idx][entity_ref.entity_idx]
        for r in range(num_rows):
            for c in range(num_cols):
                if entity.get_entity_grid_mask()[r][c]:
                    rep[r][c] = '#'
    # Apply path
    for r,c in path_item.entity_linkage_points:
        print(r,c)
        rep[r][c] = '*'
    # Convert to str
    buf = ""
    buf += "+" + "-" * (num_cols+1) + "+\n"
    for row in rep:
        buf += "|"
        for cell in row:
            buf += cell
        buf += "|\n"
    buf += "+" + "-" * (num_cols+1) + "+\n"
    print(buf)
    
    


def test_get_one_child_states_from_beginning():
    pixel_grid_str = [
        "            ",
        "            ",
        "     11     ",
        "    1111    ",
        "      11    ",
        "            ",
        "            ",
        "            ",
        "            ",
    ]
    layers, total_image_mask = helper_get_layers(pixel_grid_str)
    print("LAYERS")
    print(layers)
    # build the layers with the other code. Assume it to be correct
    test_problem = LinkerProblem(
        layers=layers,
        total_image_mask=total_image_mask,
        cost_menu=CostMenu(
            visited_mask_cost=100000,
            future_mask_cost=0,
            base_cost=1
        )
    )
    test_state = LinkerSearchState(
        cur_entity_ref=EntityReference(0, None), # Start at border
        visited_mask=get_all_false_mask(test_problem.get_num_rows(), test_problem.get_num_cols()),
        visited_layer_entity_idx_set=set(),
        cost_to_state=0,
        path=[]
    )
    # Sanity print problem
    print("Len Layers "+str(len(layers)))
    print("Len Layers[0] "+str(len(layers[0])))
    for e in layers[0]:
        print(grid_mask_to_str(e.get_entity_grid_mask()))
        print(e.get_entry_points())
    # assert False
    # Function Under Test
    recv_child_states = get_child_states(test_problem, test_state, 1)
    exp_child_states = [
        LinkerSearchState(
            cur_entity_ref=EntityReference(0, 0),
            visited_mask=[
                [False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, True,  True,  False, False, False, False, False],
                [False, False, False, False, True,  True,  True,  True,  False, False, False, False],
                [False, False, False, False, False, False, True,  True,  False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, False, False],
            ],
            visited_layer_entity_idx_set={0},
            cost_to_state=2,
            path=[PathItem([(0, 6), (1, 6), (2, 6)], EntityReference(0,0))]
        ),
    ]
    assert len(recv_child_states) == 1
    assert recv_child_states[0] == exp_child_states[0]
    

def test_get_child_states_from_beginning():
    pixel_grid_str = [
        "                  ",
        "  11      222222  ",
        " 1111      22222  ",
        "   11     2222222 ",
        "                  ",
    ]
    layers, total_image_mask = helper_get_layers(pixel_grid_str)
    print("LAYERS")
    print(layers)
    # build the layers with the other code. Assume it to be correct
    test_problem = LinkerProblem(
        layers=layers,
        total_image_mask=total_image_mask,
        cost_menu=CostMenu(
            visited_mask_cost=100000,
            future_mask_cost=0,
            base_cost=1
        )
    )
    test_state = LinkerSearchState(
        cur_entity_ref=EntityReference(0, None), # Start at border
        visited_mask=get_all_false_mask(test_problem.get_num_rows(), test_problem.get_num_cols()),
        visited_layer_entity_idx_set=set(),
        cost_to_state=0,
        path=[]
    )
    # Sanity print problem
    print("Len Layers "+str(len(layers)))
    print("Len Layers[0] "+str(len(layers[0])))
    for e in layers[0]:
        print(grid_mask_to_str(e.get_entity_grid_mask()))
        print(e.get_entry_points())
    # assert False
    # Function Under Test
    recv_child_states = get_child_states(test_problem, test_state, 2)
    exp_child_states = [
        LinkerSearchState(
            cur_entity_ref=EntityReference(0, 1),
            visited_mask=[
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  False, False],
                [False, False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  False, False],
                [False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  True,  False],
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            ],
            visited_layer_entity_idx_set={1},
            cost_to_state=1,
            path=[PathItem([(5,14), (4,14)], EntityReference(0,1))]
        ),
        LinkerSearchState(
            cur_entity_ref=EntityReference(0, 0),
            visited_mask=[
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, True,  True,  False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, True,  True,  True,  True,  False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, True,  True,  False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            ],
            visited_layer_entity_idx_set={0},
            cost_to_state=1,
            path=[PathItem([(2,0), (2,1)], EntityReference(0,0))]
        ),
    ]
    assert len(recv_child_states) == 2
    assert recv_child_states[0] == exp_child_states[0]
    assert recv_child_states[1] == exp_child_states[1]


def test_get_child_states_from_entity():
    pixel_grid_str = [
        "                  ",
        "  11      222222  ",
        " 1111      22222  ",
        "   11     2222222 ",
        "                  ",
    ]
    layers, total_image_mask = helper_get_layers(pixel_grid_str)
    print("LAYERS")
    print(layers)
    # build the layers with the other code. Assume it to be correct
    test_problem = LinkerProblem(
        layers=layers,
        total_image_mask=total_image_mask,
        cost_menu=CostMenu(
            visited_mask_cost=100000,
            future_mask_cost=0,
            base_cost=1
        )
    )
    test_state = LinkerSearchState(
        cur_entity_ref=EntityReference(0, 1),
        visited_mask=[
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  False, False],
            [False, False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  False, False],
            [False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  True,  False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
        ],
        visited_layer_entity_idx_set={1},
        cost_to_state=1,
        path=[PathItem([(0,15), (1,14)], EntityReference(0,1))]
    )
    # Sanity print problem
    print("Len Layers "+str(len(layers)))
    print("Len Layers[0] "+str(len(layers[0])))
    for e in layers[0]:
        print(grid_mask_to_str(e.get_entity_grid_mask()))
        print(e.get_entry_points())
    # Function Under Test
    recv_child_states = get_child_states(test_problem, test_state, 1)
    exp_child_states = [
        LinkerSearchState(
            cur_entity_ref=EntityReference(0, None),
            visited_mask=[
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  False, False],
                [False, False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  False, False],
                [False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  True,  False],
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            ],
            visited_layer_entity_idx_set={1},
            cost_to_state=2,
            path=[PathItem([(0,15), (1,14)], EntityReference(0,1)), PathItem([(1,16), (0,16)], EntityReference(0,None))]
        ),
        LinkerSearchState(
            cur_entity_ref=EntityReference(0, 0),
            visited_mask=[
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, True,  True,  False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  False, False],
                [False, True,  True,  True,  True,  False, False, False, False, False, False, True,  True,  True,  True,  True,  False, False],
                [False, False, False, True,  True,  False, False, False, False, False, True,  True,  True,  True,  True,  True,  True,  False],
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            ],
            visited_layer_entity_idx_set={1,0},
            cost_to_state=6,
            path=[PathItem([(0,15), (1,14)], EntityReference(0,1)), PathItem([(2, 10), (2, 9), (2, 8), (2, 7), (2, 6), (2, 5)], EntityReference(0,0))]
        ),
    ]
    assert len(recv_child_states) == 2
    assert recv_child_states[0] == exp_child_states[0]
    assert recv_child_states[1] == exp_child_states[1]


def test_get_too_many_child_states_from_entity():
    pixel_grid_str = [
        "                  ",
        "  11      222222  ",
        " 1111      22222  ",
        "   11     2222222 ",
        "                  ",
    ]
    layers, total_image_mask = helper_get_layers(pixel_grid_str)
    print("LAYERS")
    print(layers)
    # build the layers with the other code. Assume it to be correct
    test_problem = LinkerProblem(
        layers=layers,
        total_image_mask=total_image_mask,
        cost_menu=CostMenu(
            visited_mask_cost=100000,
            future_mask_cost=0,
            base_cost=1
        )
    )
    test_state = LinkerSearchState(
        cur_entity_ref=EntityReference(0, 1),
        visited_mask=[
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  False, False],
            [False, False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  False, False],
            [False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  True,  False],
            [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
        ],
        visited_layer_entity_idx_set={1},
        cost_to_state=1,
        path=[PathItem([(0,15), (1,14)], EntityReference(0,1))]
    )
    # Sanity print problem
    print("Len Layers "+str(len(layers)))
    print("Len Layers[0] "+str(len(layers[0])))
    for e in layers[0]:
        print(grid_mask_to_str(e.get_entity_grid_mask()))
        print(e.get_entry_points())
    # Function Under Test
    # Request two entity child states, enven though there is only one
    recv_child_states = get_child_states(test_problem, test_state, 2)
    exp_child_states = [
        LinkerSearchState(
            cur_entity_ref=EntityReference(0, None),
            visited_mask=[
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  False, False],
                [False, False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  False, False],
                [False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  True,  False],
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            ],
            visited_layer_entity_idx_set={1},
            cost_to_state=2,
            path=[PathItem([(0,15), (1,14)], EntityReference(0,1)), PathItem([(1,16), (0,16)], EntityReference(0,None))]
        ),
        LinkerSearchState(
            cur_entity_ref=EntityReference(0, 0),
            visited_mask=[
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, True,  True,  False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  False, False],
                [False, True,  True,  True,  True,  False, False, False, False, False, False, True,  True,  True,  True,  True,  False, False],
                [False, False, False, True,  True,  False, False, False, False, False, True,  True,  True,  True,  True,  True,  True,  False],
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
            ],
            visited_layer_entity_idx_set={1,0},
            cost_to_state=6,
            path=[PathItem([(0,15), (1,14)], EntityReference(0,1)), PathItem([(2, 10), (2, 9), (2, 8), (2, 7), (2, 6), (2, 5)], EntityReference(0,0))]
        ),
    ]
    assert len(recv_child_states) == 2
    assert recv_child_states[0] == exp_child_states[0]
    assert recv_child_states[1] == exp_child_states[1]


def test_get_child_states_entity_to_SE_border():
    pixel_grid_str = [
        "                  ",
        "                  ",
        "    111           ",
        "    111           ",
        "                  ",
        "                  ",
        "          222222  ",
        "           22222  ",
        "          2222222 ",
        "                  ",
    ]
    layers, total_image_mask = helper_get_layers(pixel_grid_str)
    print("LAYERS")
    print(layers)
    # build the layers with the other code. Assume it to be correct
    test_problem = LinkerProblem(
        layers=layers,
        total_image_mask=total_image_mask,
        cost_menu=CostMenu(
            visited_mask_cost=100000,
            future_mask_cost=0,
            base_cost=1
        )
    )
    test_state = LinkerSearchState(
        cur_entity_ref=EntityReference(0, 1),
        visited_mask=[
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
                [False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  False, False],
                [False, False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  False, False],
                [False, False, False, False, False, False, False, False, False, False, True,  True,  True,  True,  True,  True,  True,  False],
                [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False],
        ],
        visited_layer_entity_idx_set={1},
        cost_to_state=1,
        path=[]
    )
    # Sanity print problem
    print("Len Layers "+str(len(layers)))
    print("Len Layers[0] "+str(len(layers[0])))
    for e in layers[0]:
        print(grid_mask_to_str(e.get_entity_grid_mask()))
        print(e.get_entry_points())
    # Function Under Test
    recv_child_states = get_child_states(test_problem, test_state, 1)
    exp_child_states = [
        LinkerSearchState(
            cur_entity_ref=EntityReference(0, None),
            visited_mask=deepcopy(total_image_mask),
            visited_layer_entity_idx_set={1},
            cost_to_state=2,
            path=[PathItem([(0,15), (1,14)], EntityReference(0,1)), PathItem([(1,16), (0,16)], EntityReference(0,None))]
        ),
    ]
    assert len(recv_child_states) == 2
    # The path to the border will always be the zero-th element
    assert recv_child_states[0].cur_entity_ref == EntityReference(0, None)
    assert len(recv_child_states[0].path) == 1
    # assert that we get the short path to a south/east border
    # This is to test an issue where the south/east boarder was only counted as a goal at dimention+1, so it could never be reached
    assert len(recv_child_states[0].path[-1].entity_linkage_points) == 2

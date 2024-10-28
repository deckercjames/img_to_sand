
from src.linker.linker import PathItem
from src.linker.linker import EntityReference
from src.linker.linker import get_linked_path
from src.linker.linkable_entity.linkable_entity_blob import LinkableEntityBlob
from src.linker.linkable_entity.linkable_entity_line import LinkableEntityLine
from src.utils import grid_mask_to_str
from src.image_parsing.blob_extraction import get_blob_tree_nodes_from_pixel_grid
from src.consolidate_tree import consolidate_blob_trees
from src.tree import unwrap_tree_post_order_traversal
from src.linker.layer_stratagem import get_all_layer_stratagem
import numpy as np

def helper_pixel_grid_str_parser(pixel_grid_str):
    pixel_grid = []
    for line in pixel_grid_str:
        pixel_grid.append(
            [0 if c == ' ' else int(c) for c in line]
        )
    return np.array(pixel_grid)

def helper_get_layers(pixel_grid_str, num_line_erosions=0):
    pixel_grid = helper_pixel_grid_str_parser(pixel_grid_str)
    num_rows = len(pixel_grid)
    num_cols = len(pixel_grid[0])
    
    # Extract blobs
    blob_trees = get_blob_tree_nodes_from_pixel_grid(pixel_grid)
    
    # Consolidate blob trees
    consolidated_blob_tree = consolidate_blob_trees(blob_trees, num_rows, num_cols)
    
    # Unwrap consolidated blob tree
    blob_layers = unwrap_tree_post_order_traversal(consolidated_blob_tree)

    return get_all_layer_stratagem(blob_layers, num_line_errosion_itterations=num_line_erosions, num_blob_buffer_itterations=0)


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
    



def test_get_linked_path_basic():
    pixel_grid_str = [
        "                  ",
        "  11      222222  ",
        " 1111      22222  ",
        "   11     2222222 ",
        "                  ",
    ]
    layers = helper_get_layers(pixel_grid_str)
    # Function under test
    recv_linked_path = get_linked_path(layers)
    # Visual Representation
    for i, path_item in enumerate(recv_linked_path):
        print("\n{} of {}".format(i+1, len(recv_linked_path)))
        helper_print_path_item(layers, path_item)
    # exit points
    print("EXIT POINTS")
    print(layers[0][0].get_exit_points())
    print(layers[0][1].get_exit_points())
    # Expected Result
    exp_linked_path = [
        PathItem([(0,10), (1,10)], EntityReference(0,1)),
        PathItem([(2, 10), (2, 9), (2, 8), (2, 7), (2, 6), (2, 5)], EntityReference(0,0)),
    ]
    # Verify
    assert len(recv_linked_path) == len(exp_linked_path)
    for i in range(len(exp_linked_path)):
        assert recv_linked_path[i] == exp_linked_path[i]



def test_get_linked_path_nested():
    pixel_grid_str = [
        "                                  ",
        "        1111111111111             ",
        "       111111111111111            ",
        "      1111        1111111         ",
        " 11111111111         11111        ",
        " 11111111111         11111111111  ",
        " 11122221111         111111111111 ",
        " 11122221111         111112222111 ",
        " 11111111111         111222222111 ",
        " 11111111111         111222222111 ",
        "                     111222222111 ",
        "                     111111111111 ",
        "                     111111111111 ",
        "                                  ",
    ]
    layers = helper_get_layers(pixel_grid_str)
    # Sanity check test stimulus
    assert len(layers) == 2
    assert len(layers[0]) == 2
    assert len(layers[1]) == 1
    # Function under test
    recv_linked_path = get_linked_path(layers)
    # Visual Representation
    for i, path_item in enumerate(recv_linked_path):
        print("\n{} of {}".format(i+1, len(recv_linked_path)))
        helper_print_path_item(layers, path_item)
    # Verify
    assert len(recv_linked_path) == 3
    assert recv_linked_path[0].next_entity_ref == EntityReference(0, 0)
    assert recv_linked_path[1].next_entity_ref == EntityReference(0, 1)
    assert recv_linked_path[2].next_entity_ref == EntityReference(1, 0)
    assert len(recv_linked_path[0].entity_linkage_points) > 3
    assert len(recv_linked_path[1].entity_linkage_points) > 10
    assert len(recv_linked_path[2].entity_linkage_points) == 1


def test_get_linked_path_many():
    pixel_grid_str = [
        "                              111      ",
        " 1111           111111111     111      ",
        " 1111           111111111     111      ",
        "         111                           ",
        "         111      11111                ",
        "         11       11111                ",
        "         11                   1111     ",
        "                           1111111     ",
        "       1111111   111       111111      ",
        "11     1111111   111                   ",
        "11               111111                ",
        "11111            111111       11111    ",
        "11111     1111                 11111   ",
        "          1111                         ",
    ]
    layers = helper_get_layers(pixel_grid_str)
    # Sanity check test stimulus
    assert len(layers) == 1
    assert len(layers[0]) == 11
    # Function under test
    recv_linked_path = get_linked_path(layers)
    # Visual Representation
    for i, path_item in enumerate(recv_linked_path):
        print("\n{} of {}".format(i+1, len(recv_linked_path)))
        helper_print_path_item(layers, path_item)
    # Verify all entities visited
    visited_entities = set()
    for path_item in recv_linked_path:
        if path_item.next_entity_ref.entity_idx is None:
            continue
        visited_entities.add(path_item.next_entity_ref)
    assert len(visited_entities) == 11
    # assert False



def test_get_linked_path_with_line():
    pixel_grid_str = [
        "                                       ",
        "                                       ",
        "            111111111111111111         ",
        "           11               11         ",
        "           11               11         ",
        "           11               11         ",
        "          11              111111111    ",
        "       11                1111111111111 ",
        "        1               11111111111111 ",
        "        11             111111111111111 ",
        "        1              111111111111111 ",
        "       11              111111111111111 ",
        "     111               11111111111111  ",
        "   111                  1111111111111  ",
        "                                       ",
    ]
    layers = helper_get_layers(pixel_grid_str, num_line_erosions=2)
    # Sanity check test stimulus
    for i, e in enumerate(layers[0]):
        print(grid_mask_to_str(e.get_entity_grid_mask()))
    assert len(layers) == 1
    assert len(layers[0]) == 3
    assert type(layers[0][0]) == LinkableEntityLine
    assert type(layers[0][1]) == LinkableEntityBlob
    assert type(layers[0][2]) == LinkableEntityLine
    # Function under test
    recv_linked_path = get_linked_path(layers)
    # Visual Representation
    for i, path_item in enumerate(recv_linked_path):
        print("\n{} of {}".format(i+1, len(recv_linked_path)))
        helper_print_path_item(layers, path_item)
    # Verify all entities visited
    visited_entities = set()
    for path_item in recv_linked_path:
        if path_item.next_entity_ref.entity_idx is None:
            continue
        visited_entities.add(path_item.next_entity_ref)
    assert len(visited_entities) == 3


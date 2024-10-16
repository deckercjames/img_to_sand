
from src.linker.linker import get_child_states
from src.linker.linker import LinkerProblem
from src.linker.linker import CostMenu
from src.linker.linker import LinkerSearchState
from src.utils import get_all_false_mask
from src.blob_extraction import get_blob_tree_nodes_from_pixel_grid
from src.consolidate_tree import consolidate_blob_trees
from src.tree import unwrap_tree_post_order_traversal
from src.linker.layer_stratagem import get_all_layer_stratagem
from src.linker.linkable_entity.linkable_entity_blob import LinkableEntityBlob
from src.linker.linkable_entity.linkable_entity_line import LinkableEntityLine
from testing.testing_helpers import helper_grid_mask_to_string
from testing.testing_helpers import helper_pretty_mask_compare

def helper_pixel_grid_str_parser(pixel_grid_str):
    pixel_grid = []
    for line in pixel_grid_str:
        pixel_grid.append(
            [0 if c == ' ' else int(c) for c in line]
        )
    return pixel_grid

def helper_get_blob_layers(pixel_grid_str):
    pixel_grid = helper_pixel_grid_str_parser(pixel_grid_str)
    num_rows = len(pixel_grid)
    num_cols = len(pixel_grid[0])
    
    # Extract blobs
    blob_trees = get_blob_tree_nodes_from_pixel_grid(pixel_grid)
    
    # Consolidate blob trees
    consolidated_blob_tree = consolidate_blob_trees(blob_trees, num_rows, num_cols)
    
    # Unwrap consolidated blob tree
    return unwrap_tree_post_order_traversal(consolidated_blob_tree)


def test_get_all_layer_strats_basic():
    pixel_grid_str = [
        "                  ",
        "  11      222222  ",
        " 1111      22222  ",
        "   111    2222222 ",
        "                  ",
    ]
    blob_layers = helper_get_blob_layers(pixel_grid_str)
    # Call function under test
    recv_layer_strats = get_all_layer_stratagem(blob_layers, num_line_errosion_itterations=0, num_blob_buffer_itterations=0)
    # Define expected output
    exp_layer_ent_0 = \
        "                  \n" \
        "  ##              \n" \
        " ####             \n" \
        "   ###            \n" \
        "                  \n"
    exp_layer_ent_1 = \
        "                  \n" \
        "          ######  \n" \
        "           #####  \n" \
        "          ####### \n" \
        "                  \n"
    # Assert
    assert len(recv_layer_strats) == 1
    assert len(recv_layer_strats[0]) == 2
    assert type(recv_layer_strats[0][0]) == LinkableEntityBlob
    assert type(recv_layer_strats[0][1]) == LinkableEntityBlob
    assert helper_grid_mask_to_string(recv_layer_strats[0][0].get_entity_grid_mask()) == exp_layer_ent_0
    assert helper_grid_mask_to_string(recv_layer_strats[0][1].get_entity_grid_mask()) == exp_layer_ent_1
    


def test_get_all_layer_strats_complex():
    pixel_grid_str = [
        "                   22222      ",
        "  11          222222222222    ",
        " 1111      2222222222222222222",
        "  1111     2222211111112222222",
        " 11111    22222211111112222222",
        "  1111    222221111111122222  ",
        "           22222222222222222  ",
        "              2222222222222   ",
        "     2222222222222222222      ",
    ]
    blob_layers = helper_get_blob_layers(pixel_grid_str)
    # Call function under test
    recv_layer_strats = get_all_layer_stratagem(blob_layers, num_line_errosion_itterations=0, num_blob_buffer_itterations=0)
    # Define expected output
    exp_layer_ent_l0_e0 = [
        "                              ",
        "                              ",
        "                              ",
        "                #######       ",
        "                #######       ",
        "               ########       ",
        "                              ",
        "                              ",
        "                              ",
    ]
    exp_layer_ent_l1_e0 = [
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "                              ",
        "     ######                   ",
    ]
    exp_layer_ent_l1_e1 = [
        "                   #####      ",
        "              ############    ",
        "           ###################",
        "           #####       #######",
        "          ######       #######",
        "          #####        #####  ",
        "           #################  ",
        "              #############   ",
        "           #############      ",
    ]
    exp_layer_ent_l1_e2 = [
        "                              ",
        "  ##                          ",
        " ####                         ",
        "  ####                        ",
        " #####                        ",
        "  ####                        ",
        "                              ",
        "                              ",
        "                              ",
    ]
    # Assert
    assert len(recv_layer_strats) == 2
    assert len(recv_layer_strats[0]) == 1
    assert len(recv_layer_strats[1]) == 3
    assert type(recv_layer_strats[0][0]) == LinkableEntityBlob
    assert type(recv_layer_strats[1][0]) == LinkableEntityLine
    assert type(recv_layer_strats[1][1]) == LinkableEntityBlob
    assert type(recv_layer_strats[1][2]) == LinkableEntityBlob
    result = [
        helper_pretty_mask_compare(exp_layer_ent_l0_e0, recv_layer_strats[0][0].get_entity_grid_mask()),
        helper_pretty_mask_compare(exp_layer_ent_l1_e0, recv_layer_strats[1][0].get_entity_grid_mask()),
        helper_pretty_mask_compare(exp_layer_ent_l1_e1, recv_layer_strats[1][1].get_entity_grid_mask()),
        helper_pretty_mask_compare(exp_layer_ent_l1_e2, recv_layer_strats[1][2].get_entity_grid_mask()),
    ]
    assert all(result)
    

def test_get_all_layer_strats_complex2():
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
    blob_layers = helper_get_blob_layers(pixel_grid_str)
    # Call function under test
    recv_layer_strats = get_all_layer_stratagem(blob_layers, num_line_errosion_itterations=2, num_blob_buffer_itterations=0)
    # Define expected output
    exp_layer_ent_0 = [
        "                                       ",
        "                                       ",
        "            #################          ",
        "            #                          ",
        "           #                           ",
        "           #                           ",
        "           #                           ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
    ]
    exp_layer_ent_1 = [
        "                                       ",
        "                                       ",
        "                                       ",
        "                            ##         ",
        "                            ##         ",
        "                            ##         ",
        "                          #########    ",
        "                         ############# ",
        "                        ############## ",
        "                       ############### ",
        "                       ############### ",
        "                       ############### ",
        "                       ##############  ",
        "                        #############  ",
        "                                       ",
    ]
    exp_layer_ent_2 = [
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "                                       ",
        "        #                              ",
        "        #                              ",
        "        #                              ",
        "        #                              ",
        "       ##                              ",
        "     ###                               ",
        "   ###                                 ",
        "                                       ",
    ]
    # Assert
    assert len(recv_layer_strats) == 1
    assert len(recv_layer_strats[0]) == 3
    assert type(recv_layer_strats[0][0]) == LinkableEntityLine
    assert type(recv_layer_strats[0][1]) == LinkableEntityBlob
    assert type(recv_layer_strats[0][2]) == LinkableEntityLine
    result = [
        helper_pretty_mask_compare(exp_layer_ent_0, recv_layer_strats[0][0].get_entity_grid_mask()),
        helper_pretty_mask_compare(exp_layer_ent_1, recv_layer_strats[0][1].get_entity_grid_mask()),
        helper_pretty_mask_compare(exp_layer_ent_2, recv_layer_strats[0][2].get_entity_grid_mask()),
    ]
    assert all(result)
    

from src.path_elaboration.elaborator_blob import convert_topography_to_elaborator_tree
from src.path_elaboration.elaborator_blob import elaborate_blob
from src.tree import TreeNode
from src.linker.linkable_entity.linkable_entity_blob import get_blob_linkable_entity
from src.linker.linkable_entity.topography import get_all_blobs_from_mask
from src.tree import TreeNode

def helper_blob_from_str_rep(str_rep):
    assert len(str_rep) > 0, "BAD TEST: str_rep must have at lest one line"
    assert all([len(line) == len(str_rep[0]) for line in str_rep]), "BAD TEST: All lines in str rep must be the same length"
    grid_mask = []
    for line in str_rep:
        grid_mask.append([False if c == ' ' else True for c in line])
    blobs = get_all_blobs_from_mask(grid_mask)
    assert len(blobs) == 1, "BAD TEST: Can only extract one blob"
    return blobs[0]


def helper_get_path_visual(path, num_rows, num_cols):
    
    # break the contour list into a grid of horizontal and vertical boundaries ("fences")
    hor_fences  = [[False for _ in range(num_cols)] for _ in range(num_rows + 1)]
    vert_fences = [[False for _ in range(num_cols + 1)] for _ in range(num_rows)]
    
    # populate fence tables
    for i in range(len(path)-1):
        r, c = path[i+1]
        prev_r, prev_c = path[i]
        if r == prev_r and c == prev_c:
            continue
        if r == prev_r:
            hor_fences[r][min(c, prev_c)] = True
        elif c == prev_c:
            vert_fences[min(r, prev_r)][c] = True
        else:
            raise Exception("Somethiing has gone horribally wrong")
    
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



def test_convert_topograph_basic():
    test_tree = TreeNode(
        node_data="Hello",
        children=[
            TreeNode(
                node_data="World",
                children=[]
            )
        ]
    )
    # Function under test
    result_tree = convert_topography_to_elaborator_tree(test_tree)
    print(result_tree)


def test_elaborate_blob_basic():
    test_mask_str_rep = [
        "  ##############################     ",
        "  ################################   ",
        "#################################### ",
        "#################################### ",
        "#################################### ",
        "#####################################",
        "#####################################",
        "##################################   ",
        "##################################   ",
        "##################################   ",
        "##################################   ",
        "##################################   ",
        "#####################################",
        "#####################################",
        " ####################################",
        " ####################################",
        "  ###################################",
        "             ####################### ",
    ]
    num_rows = len(test_mask_str_rep)
    num_cols = len(test_mask_str_rep[0])
    blob = helper_blob_from_str_rep(test_mask_str_rep)
    linkable_entity = get_blob_linkable_entity(blob)
    # Function under test
    recv_elaborated_path = elaborate_blob(linkable_entity, (0,2), None, 2)
    assert recv_elaborated_path is not None
    # Visualize output
    recv_str_rep = helper_get_path_visual(recv_elaborated_path, num_rows, num_cols)
    print(recv_str_rep)
    # Define expected behavior
    exp_str_rep = \
        "+  +  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+  +  +  +  +  +\n" \
        "      |  |                                                                                      |               \n" \
        "+  +  +  +--+  +  +  +  +  +  +  +  +  +  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+  +--+--+  +  +  +\n" \
        "      |     |                             |                                                  |        |         \n" \
        "+--+--+  +  +--+--+--+--+--+--+--+--+--+--+  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +--+--+  +--+--+  +\n" \
        "|           |  |                                                                                   |        |   \n" \
        "+  +  +  +  +  +--+  +  +  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+  +  +  +  +--+--+  +  +\n" \
        "|           |     |        |                                                           |                 |  |   \n" \
        "+  +  +--+--+  +  +--+--+--+  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +--+--+  +  +  +  +  +  +\n" \
        "|     |           |  |                                                                       |           |  |   \n" \
        "+  +  +  +  +  +  +  +--+  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+  +  +  +  +  +  +  +  +  +--+\n" \
        "|     |           |     |  |                                                     |           |           |     |\n" \
        "+  +  +  +  +--+--+  +  +--+  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +  +--+--+  +  +  +  +--+--+  +  +\n" \
        "|     |     |           |  |                                                           |     |     |           |\n" \
        "+  +  +  +  +  +  +  +  +  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+  +  +  +  +  +  +  +  +  +--+--+--+\n" \
        "|     |     |           |     |                                            |           |     |     |  |         \n" \
        "+  +  +  +  +  +  +  +--+  +  +--+--+--+--+--+--+--+--+--+--+--+--+--+--+  +--+--+  +  +  +  +  +  +  +  +  +  +\n" \
        "|     |     |        |        |                                         |        |     |     |     |  |         \n" \
        "+  +  +  +  +  +  +  +  +  +  +--+--+--+--+--+--+--+--+--+--+--+  +  +  +--+--+  +  +  +  +  +  +  +  +  +  +  +\n" \
        "|     |     |        |                                         |              |  |     |     |     |  |         \n" \
        "+  +  +  +  +--+  +  +--+  +  +  +  +  +  +  +  +  +  +  +  +  +--+--+--+--+--+  +  +  +  +  +  +  +  +  +  +  +\n" \
        "|     |        |        |                                                        |     |     |     |  |         \n" \
        "+  +  +  +  +  +  +  +  +--+--+--+--+--+--+--+--+--+--+--+  +  +  +  +  +  +  +--+  +  +  +  +  +  +  +  +  +  +\n" \
        "|     |        |                                         |                    |        |     |     |  |         \n" \
        "+  +  +--+  +  +--+  +  +  +  +  +  +  +  +  +  +  +  +  +--+--+--+--+--+--+--+  +  +  +  +  +  +  +  +--+--+--+\n" \
        "|        |        |                                                                    |     |     |           |\n" \
        "+  +  +  +  +  +  +--+--+--+--+--+--+--+--+--+--+--+  +  +  +  +  +  +  +  +--+--+--+--+  +  +  +  +--+--+--+  +\n" \
        "|        |                                         |                       |                 |              |  |\n" \
        "+--+  +  +--+  +  +  +  +  +  +  +  +  +  +  +  +  +--+--+--+--+--+--+--+--+  +  +  +  +  +  +  +  +  +  +  +  +\n" \
        "   |        |                                                                                |              |  |\n" \
        "+  +  +  +  +--+--+--+--+--+--+--+--+--+--+--+  +  +  +  +  +  +  +  +  +  +--+--+--+--+--+--+  +  +  +  +  +  +\n" \
        "   |                                         |                             |                                |  |\n" \
        "+  +--+  +  +  +  +  +  +  +  +  +  +  +  +  +--+--+--+--+--+--+--+--+--+--+  +  +  +  +  +  +  +  +  +  +--+  +\n" \
        "      |                                                                                                  |     |\n" \
        "+  +  +--+--+--+--+--+--+--+--+--+--+--+  +  +  +  +  +  +  +  +  +  +  +  +--+--+--+--+--+--+--+--+--+--+  +--+\n" \
        "                                       |                                   |                                |   \n" \
        "+  +  +  +  +  +  +  +  +  +  +  +  +  +--+--+--+--+--+--+--+--+--+--+--+--+  +--+--+--+--+--+--+--+--+--+--+  +\n"
    # Validate
    assert recv_str_rep == exp_str_rep

# TODO reenable. Maybe fix intermediat blob with long tail
# def test_elaborate_blob_basic():
#     test_mask_str_rep = [
#         "  ##############################     ",
#         "  ################################   ",
#         "#################################### ",
#         "#################################### ",
#         "#################################### ",
#         "#######        ######################",
#         "#######        ######################",
#         "########     #####################   ",
#         "########     #####################   ",
#         "##################################   ",
#         "##################################   ",
#         "##################################   ",
#         "#####################################",
#         "#####################################",
#         " ####################################",
#         " ####################################",
#         "  ###################################",
#         "             ####################### ",
#     ]
#     num_rows = len(test_mask_str_rep)
#     num_cols = len(test_mask_str_rep[0])
#     blob = helper_blob_from_str_rep(test_mask_str_rep)
#     linkable_entity = get_blob_linkable_entity(blob, 1)
#     # Function under test
#     recv_elaborated_path = elaborate_blob(linkable_entity, (0,2), None, 2)
#     assert recv_elaborated_path is not None
#     print("RECEIVED PATH")
#     print(recv_elaborated_path)
#     # Visualize output
#     recv_str_rep = helper_get_path_visual(recv_elaborated_path, num_rows, num_cols)
#     print(recv_str_rep)
#     print(get_topography_tree_visual(linkable_entity.blob_topography, num_rows, num_cols))
#     assert False


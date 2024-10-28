

from src.linker.linkable_entity.topography import get_blob_topography
from src.linker.linkable_entity.topography import get_all_blobs_from_mask
from src.linker.linkable_entity.topography import get_topography_tree_visual
from src.tree import TreeNode
import numpy as np

def blob_from_str_rep_helper(str_rep):
    assert len(str_rep) > 0, "BAD TEST: str_rep must have at lest one line"
    assert all([len(line) == len(str_rep[0]) for line in str_rep]), "BAD TEST: All lines in str rep must be the same length"
    grid_mask = []
    for line in str_rep:
        grid_mask.append([False if c == ' ' else True for c in line])
    blobs = get_all_blobs_from_mask(np.array(grid_mask))
    assert len(blobs) == 1, "BAD TEST: Can only extract one blob"
    return blobs[0]


def test_blob_topography_3x3():
    test_mask_str_rep = [
        "     ",
        " ### ",
        " ### ",
        " ### ",
        "     ",
    ]
    blob = blob_from_str_rep_helper(test_mask_str_rep)
    recv_blob_topography = get_blob_topography(blob)
    exp_topography = TreeNode(
        [(1,1), (1,2), (1,3), (1,4), (2,4), (3,4), (4,4), (4,3), (4,2), (4,1), (3,1), (2,1)],
        children=[
            TreeNode(
                [(2,2), (2,3), (3,3), (3,2)]
            )
        ]
    )
    assert recv_blob_topography == exp_topography


def test_blob_topography_3x3_at_edge():
    test_mask_str_rep = [
        "###",
        "###",
        "###",
    ]
    blob = blob_from_str_rep_helper(test_mask_str_rep)
    recv_blob_topography = get_blob_topography(blob)
    exp_topography = TreeNode(
        [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0), (2,0), (1,0)],
        children=[
            TreeNode(
                [(1,1), (1,2), (2,2), (2,1)]
            )
        ]
    )
    assert recv_blob_topography == exp_topography


def test_blob_topography_3x3_with_void():
    test_mask_str_rep = [
        "     ",
        " ### ",
        " # # ",
        " ### ",
        "     ",
    ]
    blob = blob_from_str_rep_helper(test_mask_str_rep)
    recv_blob_topography = get_blob_topography(blob)
    exp_topography = TreeNode(
        [(1,1), (1,2), (1,3), (1,4), (2,4), (3,4), (4,4), (4,3), (4,2), (4,1), (3,1), (2,1)],
        children=[
            TreeNode(
                [(2,2), (2,3), (3,3), (3,2)]
            )
        ]
    )
    assert recv_blob_topography == exp_topography


def test_blob_topography_5x5():
    test_mask_str_rep = [
        "       ",
        " ##### ",
        " ##### ",
        " ##### ",
        " ##### ",
        " ##### ",
        "       ",
    ]
    blob = blob_from_str_rep_helper(test_mask_str_rep)
    recv_topography_tree = get_blob_topography(blob)
    recv_topography_visual_rep = get_topography_tree_visual(recv_topography_tree, len(test_mask_str_rep), len(test_mask_str_rep[0]))
    expedted_topography_visual_rep = \
    "+  +  +  +  +  +  +  +\n" \
    "                      \n" \
    "+  +--+--+--+--+--+  +\n" \
    "   |              |   \n" \
    "+  +  +--+--+--+  +  +\n" \
    "   |  |        |  |   \n" \
    "+  +  +  +--+  +  +  +\n" \
    "   |  |  |  |  |  |   \n" \
    "+  +  +  +--+  +  +  +\n" \
    "   |  |        |  |   \n" \
    "+  +  +--+--+--+  +  +\n" \
    "   |              |   \n" \
    "+  +--+--+--+--+--+  +\n" \
    "                      \n" \
    "+  +  +  +  +  +  +  +\n"
    assert recv_topography_visual_rep == expedted_topography_visual_rep


def test_blob_topography_5x5_large_void():
    test_mask_str_rep = [
        "       ",
        " ##### ",
        " #   # ",
        " #   # ",
        " #   # ",
        " ##### ",
        "       ",
    ]
    blob = blob_from_str_rep_helper(test_mask_str_rep)
    recv_topography_tree = get_blob_topography(blob)
    recv_topography_visual_rep = get_topography_tree_visual(recv_topography_tree, len(test_mask_str_rep), len(test_mask_str_rep[0]))
    expedted_topography_visual_rep = \
    "+  +  +  +  +  +  +  +\n" \
    "                      \n" \
    "+  +--+--+--+--+--+  +\n" \
    "   |              |   \n" \
    "+  +  +--+--+--+  +  +\n" \
    "   |  |        |  |   \n" \
    "+  +  +  +  +  +  +  +\n" \
    "   |  |        |  |   \n" \
    "+  +  +  +  +  +  +  +\n" \
    "   |  |        |  |   \n" \
    "+  +  +--+--+--+  +  +\n" \
    "   |              |   \n" \
    "+  +--+--+--+--+--+  +\n" \
    "                      \n" \
    "+  +  +  +  +  +  +  +\n"
    assert recv_topography_visual_rep == expedted_topography_visual_rep


def test_blob_topography_hourglass():
    test_mask_str_rep = [
        "#######",
        " ##### ",
        "  ###  ",
        "   #   ",
        "  ###  ",
        " ##### ",
        "#######",
    ]
    blob = blob_from_str_rep_helper(test_mask_str_rep)
    recv_topography_tree = get_blob_topography(blob)
    recv_topography_visual_rep = get_topography_tree_visual(recv_topography_tree, len(test_mask_str_rep), len(test_mask_str_rep[0]))
    expedted_topography_visual_rep = \
    "+--+--+--+--+--+--+--+\n" \
    "|                    |\n" \
    "+--+  +  +--+  +  +--+\n" \
    "   |     |  |     |   \n" \
    "+  +--+  +--+  +--+  +\n" \
    "      |        |      \n" \
    "+  +  +--+  +--+  +  +\n" \
    "         |  |         \n" \
    "+  +  +--+  +--+  +  +\n" \
    "      |        |      \n" \
    "+  +--+  +--+  +--+  +\n" \
    "   |     |  |     |   \n" \
    "+--+  +  +--+  +  +--+\n" \
    "|                    |\n" \
    "+--+--+--+--+--+--+--+\n"
    print("RECEIVED")
    print(recv_topography_visual_rep)
    assert recv_topography_visual_rep == expedted_topography_visual_rep


def test_blob_topography_two_voids():
    test_mask_str_rep = [
        "#########",
        "#########",
        "#########",
        "###  ####",
        "###  ####",
        "#########",
        "####  ###",
        "####  ###",
        "#########",
        "#########",
        "#########",
    ]
    blob = blob_from_str_rep_helper(test_mask_str_rep)
    recv_topography_tree = get_blob_topography(blob)
    recv_topography_visual_rep = get_topography_tree_visual(recv_topography_tree, len(test_mask_str_rep), len(test_mask_str_rep[0]))
    expedted_topography_visual_rep = \
    "+--+--+--+--+--+--+--+--+--+\n" \
    "|                          |\n" \
    "+  +--+--+--+--+--+--+--+  +\n" \
    "|  |                    |  |\n" \
    "+  +  +--+--+--+--+  +  +  +\n" \
    "|  |  |           |     |  |\n" \
    "+  +  +  +--+--+  +  +  +  +\n" \
    "|  |  |  |     |  |     |  |\n" \
    "+  +  +  +  +  +  +  +  +  +\n" \
    "|  |  |  |     |  |     |  |\n" \
    "+  +  +  +--+--+  +--+  +  +\n" \
    "|  |  |              |  |  |\n" \
    "+  +  +--+  +--+--+  +  +  +\n" \
    "|  |     |  |     |  |  |  |\n" \
    "+  +  +  +  +  +  +  +  +  +\n" \
    "|  |     |  |     |  |  |  |\n" \
    "+  +  +  +  +--+--+  +  +  +\n" \
    "|  |     |           |  |  |\n" \
    "+  +  +  +--+--+--+--+  +  +\n" \
    "|  |                    |  |\n" \
    "+  +--+--+--+--+--+--+--+  +\n" \
    "|                          |\n" \
    "+--+--+--+--+--+--+--+--+--+\n"
    print("RECEIVED")
    print(recv_topography_visual_rep)
    assert recv_topography_visual_rep == expedted_topography_visual_rep


def test_blob_topography_hourglass_two_voids():
    test_mask_str_rep = [
        "######",
        "##  ##",
        "##  ##",
        "######",
        " #### ",
        "  ##  ",
        " #### ",
        "######",
        "##  ##",
        "##  ##",
        "######",
    ]
    blob = blob_from_str_rep_helper(test_mask_str_rep)
    recv_topography_tree = get_blob_topography(blob)
    recv_topography_visual_rep = get_topography_tree_visual(recv_topography_tree, len(test_mask_str_rep), len(test_mask_str_rep[0]))
    expedted_topography_visual_rep = \
    "+--+--+--+--+--+--+\n" \
    "|                 |\n" \
    "+  +  +--+--+  +  +\n" \
    "|     |     |     |\n" \
    "+  +  +  +  +  +  +\n" \
    "|     |     |     |\n" \
    "+  +  +--+--+  +  +\n" \
    "|                 |\n" \
    "+--+  +  +  +  +--+\n" \
    "   |           |   \n" \
    "+  +--+  +  +--+  +\n" \
    "      |     |      \n" \
    "+  +--+  +  +--+  +\n" \
    "   |           |   \n" \
    "+--+  +  +  +  +--+\n" \
    "|                 |\n" \
    "+  +  +--+--+  +  +\n" \
    "|     |     |     |\n" \
    "+  +  +  +  +  +  +\n" \
    "|     |     |     |\n" \
    "+  +  +--+--+  +  +\n" \
    "|                 |\n" \
    "+--+--+--+--+--+--+\n"
    print("RECEIVED")
    print(recv_topography_visual_rep)
    assert recv_topography_visual_rep == expedted_topography_visual_rep

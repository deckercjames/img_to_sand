
from src.consolidate_tree import consolidate_blob_trees
from src.consolidate_tree import ConsolidatedTreeData
from src.tree import TreeNode
from src.blob_extraction import Blob

def test_consol_tree_empy_list():
    test_blob_trees = []
    received_tree = consolidate_blob_trees(test_blob_trees, 2, 2)
    assert received_tree is None


def test_consol_tree_basic():
    test_blob_trees = [
        TreeNode(
            Blob(
                # Outer contour
                [(0,1), (0,2), (1,2), (1,1)],
                # Blob mask
                [
                    [False, True ],
                    [False, False],
                ],
                # Total mask (unused for the tested funciton)
                None
            ),
            # Sub-blobs
            [],
        ),
        TreeNode(
            Blob(
                # Outer contour
                [(1,0), (1,1), (2,1), (2,0)],
                # Blob mask
                [
                    [False, False],
                    [True,  False],
                ],
                # Total mask (unused for the tested funciton)
                None
            ),
            # Sub-blobs
            [],
        ),
    ]
    expected_tree = TreeNode(
        ConsolidatedTreeData(
            # Parental blob mask
            [
                [False, False],
                [False, False],
            ],
            # Blob list
            [
                Blob(
                    # Outer contour
                    [(0,1), (0,2), (1,2), (1,1)],
                    # Blob mask
                    [
                        [False, True ],
                        [False, False],
                    ],
                    # Total mask (unused for the tested funciton)
                    None
                ),
                Blob(
                    # Outer contour
                    [(1,0), (1,1), (2,1), (2,0)],
                    # Blob mask
                    [
                        [False, False],
                        [True,  False],
                    ],
                    # Total mask (unused for the tested funciton)
                    None
                ),
            ]
        ),
        # No children
        []
    )
    received_tree = consolidate_blob_trees(test_blob_trees, 2, 2)
    assert received_tree == expected_tree
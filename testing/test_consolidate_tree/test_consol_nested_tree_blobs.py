
from src.consolidate_tree import consolidate_blob_trees
from src.tree import TreeNode
from src.blob_extraction import Blob


def test_consol_tree_nested():
    test_blob_trees = [
        TreeNode(
            Blob(
                # Outer contour (unused for the tested function)
                None,
                # Blob mask
                [
                    [True,  True,  True,  True,  True],
                    [True,  False, False, False, True],
                    [True,  False, False, False, True],
                    [True,  False, False, False, True],
                    [True,  True,  True,  True,  True],
                ],
                # Total mask (unused for the tested function)
                None
            ),
            # Tree node children
            [
                TreeNode(
                    Blob(
                        # Outer contour (unused for the tested function)
                        None,
                        # Blob mask
                        [
                            [False, False, False, False, False],
                            [False, True,  True,  True,  False],
                            [False, True,  False, True,  False],
                            [False, True,  True,  True,  False],
                            [False, False, False, False, False],
                        ],
                        # Total mask (unused for the tested function)
                        None
                    ),
                    # Tree node children
                    [
                        TreeNode(
                            Blob(
                                # Outer contour (unused for the tested function)
                                None,
                                # Blob mask
                                [
                                    [False, False, False, False, False],
                                    [False, False, False, False, False],
                                    [False, False, True,  False, False],
                                    [False, False, False, False, False],
                                    [False, False, False, False, False],
                                ],
                                # Total mask (unused for the tested function)
                                None
                            ),
                            # No tree node children
                            []
                        )
                    ],
                ),
            ],
        ),
    ]
    expected_tree = TreeNode(
        # Blob list
        [
            Blob(
                # Outer contour (unused for the tested function)
                None,
                # Blob mask
                [
                    [True,  True,  True,  True,  True],
                    [True,  False, False, False, True],
                    [True,  False, False, False, True],
                    [True,  False, False, False, True],
                    [True,  True,  True,  True,  True],
                ],
                # Total mask (unused for the tested function)
                None
            ),
        ],
        # Tree node children
        [
            TreeNode(
                # Blob list
                [
                    Blob(
                        # Outer contour (unused for the tested function)
                        None,
                        # Blob mask
                        [
                            [False, False, False, False, False],
                            [False, True,  True,  True,  False],
                            [False, True,  False, True,  False],
                            [False, True,  True,  True,  False],
                            [False, False, False, False, False],
                        ],
                        # Total mask (unused for the tested function)
                        None
                    ),
                ],
                # Tree node children
                [
                    TreeNode(
                        # Blob list
                        [
                            Blob(
                                # Outer contour (unused for the tested function)
                                None,
                                # Blob mask
                                [
                                    [False, False, False, False, False],
                                    [False, False, False, False, False],
                                    [False, False, True,  False, False],
                                    [False, False, False, False, False],
                                    [False, False, False, False, False],
                                ],
                                # Total mask (unused for the tested function)
                                None
                            ),
                        ],
                        # No tree node children
                        []
                    )
                ]
            )
        ]
    )
    received_tree = consolidate_blob_trees(test_blob_trees, 5, 5)
    assert received_tree == expected_tree
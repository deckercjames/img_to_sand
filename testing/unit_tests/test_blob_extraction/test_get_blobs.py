
from src.image_parsing.blob_extraction import get_blob_tree_nodes_from_pixel_grid
from src.image_parsing.blob_extraction import Blob
from src.tree import TreeNode
from copy import deepcopy
import numpy as np


def test_get_blobs_basic():
    test_pixel_grid = [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    test_pixel_grid = np.array(test_pixel_grid)
    test_pixel_grid_unchanged = test_pixel_grid.copy()
    recv_blobs = get_blob_tree_nodes_from_pixel_grid(test_pixel_grid)
    expected_blobs = [
        TreeNode(
            Blob(
                # Outer contour
                [(1,2), (1,3), (1,4), (2,4), (2,3), (2,2)],
                # Blob mask
                np.array([
                    [False, False, False, False, False],
                    [False, False, True,  True,  False],
                    [False, False, False, False, False],
                ]),
                # Total mask
                np.array([
                    [False, False, False, False, False],
                    [False, False, True,  True,  False],
                    [False, False, False, False, False],
                ]),
            ),
            # Children
            []
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert (test_pixel_grid == test_pixel_grid_unchanged).all()


def test_get_blobs_two():
    test_pixel_grid = [
        [0, 1],
        [1, 0],
    ]
    test_pixel_grid = np.array(test_pixel_grid)
    test_pixel_grid_unchanged = test_pixel_grid.copy()
    recv_blobs = get_blob_tree_nodes_from_pixel_grid(test_pixel_grid)
    expected_blobs = [
        TreeNode(
            Blob(
                # Outer contour
                [(0,1), (0,2), (1,2), (1,1)],
                # Blob mask
                np.array([
                    [False, True ],
                    [False, False],
                ]),
                # Total mask
                np.array([
                    [False, True ],
                    [False, False],
                ]),
            ),
            # Sub-blobs
            [],
        ),
        TreeNode(
            Blob(
                # Outer contour
                [(1,0), (1,1), (2,1), (2,0)],
                # Blob mask
                np.array([
                    [False, False],
                    [True,  False],
                ]),
                # Total mask
                np.array([
                    [False, False],
                    [True,  False],
                ]),
            ),
            # Sub-blobs
            [],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert (test_pixel_grid == test_pixel_grid_unchanged).all()


def test_get_two_blobs_adjacent():
    test_pixel_grid = [
        [1, 2],
    ]
    test_pixel_grid = np.array(test_pixel_grid)
    test_pixel_grid_unchanged = test_pixel_grid.copy()
    recv_blobs = get_blob_tree_nodes_from_pixel_grid(test_pixel_grid)
    expected_blobs = [
        TreeNode(
            Blob(
                # Outer contour
                [(0,0), (0,1), (1,1), (1,0)],
                # Blob mask
                np.array([
                    [True, False],
                ]),
                # Total mask
                np.array([
                    [True, False],
                ]),
            ),
            # Sub-blobs
            [],
        ),
        TreeNode(
            Blob(
                # Outer contour
                [(0,1), (0,2), (1,2), (1,1)],
                # Blob mask
                np.array([
                    [False, True],
                ]),
                # Total mask
                np.array([
                    [False, True],
                ]),
            ),
            # Sub-blobs
            [],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert (test_pixel_grid == test_pixel_grid_unchanged).all()


def test_get_blobs_one_with_void():
    test_pixel_grid = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    test_pixel_grid = np.array(test_pixel_grid)
    test_pixel_grid_unchanged = test_pixel_grid.copy()
    recv_blobs = get_blob_tree_nodes_from_pixel_grid(test_pixel_grid)
    expected_blobs = [
        TreeNode(
            Blob(
                # Outer contour
                [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0), (2,0), (1,0)],
                # Blob mask
                np.array([
                    [True,  True,  True],
                    [True,  False, True],
                    [True,  True,  True],
                ]),
                # Total mask
                np.array([
                    [True,  True,  True],
                    [True,  True,  True],
                    [True,  True,  True],
                ]),
            ),
            # Sub-blobs
            [],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert (test_pixel_grid == test_pixel_grid_unchanged).all()


def test_get_blobs_one_with_two_voids():
    test_pixel_grid = [
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
    ]
    test_pixel_grid = np.array(test_pixel_grid)
    test_pixel_grid_unchanged = test_pixel_grid.copy()
    recv_blobs = get_blob_tree_nodes_from_pixel_grid(test_pixel_grid)
    expected_blobs = [
        TreeNode(
            Blob(
                # Outer contour
                [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,5), (2,5), (3,5), (3,4), (3,3), (3,2), (3,1), (3,0), (2,0), (1,0)],
                # Blob mask
                np.array([
                    [True,  True,  True,  True,  True],
                    [True,  False, True,  False, True],
                    [True,  True,  True,  True,  True],
                ]),
                # Total mask
                np.array([
                    [True,  True,  True,  True,  True],
                    [True,  True,  True,  True,  True],
                    [True,  True,  True,  True,  True],
                ]),
            ),
            # Sub-blobs
            [],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert (test_pixel_grid == test_pixel_grid_unchanged).all()


def test_get_blobs_nested():
    test_pixel_grid = [
        [1, 1, 1],
        [1, 2, 1],
        [1, 1, 1],
    ]
    test_pixel_grid = np.array(test_pixel_grid)
    test_pixel_grid_unchanged = test_pixel_grid.copy()
    recv_blobs = get_blob_tree_nodes_from_pixel_grid(test_pixel_grid)
    expected_blobs = [
        TreeNode(
            Blob(
                # Outer contour
                [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0), (2,0), (1,0)],
                # Blob mask
                np.array([
                    [True,  True,  True],
                    [True,  False, True],
                    [True,  True,  True],
                ]),
                # Total mask
                np.array([
                    [True,  True,  True],
                    [True,  True,  True],
                    [True,  True,  True],
                ]),
            ),
            # Sub-blobs
            [
                TreeNode(
                    Blob(
                        # Outer contour
                        [(1,1), (1,2), (2,2), (2,1)],
                        # Blob mask
                        np.array([
                            [False, False, False],
                            [False, True,  False],
                            [False, False, False],
                        ]),
                        # Total mask
                        np.array([
                            [False, False, False],
                            [False, True,  False],
                            [False, False, False],
                        ]),
                    ),
                    # Sub-blobs
                    [],
                ),
            ],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert (test_pixel_grid == test_pixel_grid_unchanged).all()



def test_get_blobs_nested_with_void_buffer():
    test_pixel_grid = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 2, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]
    test_pixel_grid = np.array(test_pixel_grid)
    test_pixel_grid_unchanged = test_pixel_grid.copy()
    recv_blobs = get_blob_tree_nodes_from_pixel_grid(test_pixel_grid)
    expected_blobs = [
        TreeNode(
            Blob(
                # Outer contour
                [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,5), (2,5), (3,5), (4,5), (5,5), (5,4), (5,3), (5,2), (5,1), (5,0), (4,0), (3,0), (2,0), (1,0)],
                # Blob mask
                np.array([
                    [True,  True,  True,  True,  True],
                    [True,  False, False, False, True],
                    [True,  False, False, False, True],
                    [True,  False, False, False, True],
                    [True,  True,  True,  True,  True],
                ]),
                # Total mask
                np.array([
                    [True,  True,  True,  True,  True],
                    [True,  True,  True,  True,  True],
                    [True,  True,  True,  True,  True],
                    [True,  True,  True,  True,  True],
                    [True,  True,  True,  True,  True],
                ]),
            ),
            # Sub-blobs
            [
                TreeNode(
                    Blob(
                        # Outer contour
                        [(2,2), (2,3), (3,3), (3,2)],
                        # Blob mask
                        np.array([
                            [False, False, False, False, False],
                            [False, False, False, False, False],
                            [False, False, True,  False, False],
                            [False, False, False, False, False],
                            [False, False, False, False, False],
                        ]),
                        # Total mask
                        np.array([
                            [False, False, False, False, False],
                            [False, False, False, False, False],
                            [False, False, True,  False, False],
                            [False, False, False, False, False],
                            [False, False, False, False, False],
                        ]),
                    ),
                    # Sub-blobs
                    [],
                ),
            ],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert (test_pixel_grid == test_pixel_grid_unchanged).all()


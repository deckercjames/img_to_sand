
from src.blob_extraction import get_blobs
from src.blob_extraction import BlobTuple
from copy import deepcopy


def test_get_blobs_basic():
    test_pixel_grid = [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    test_pixel_grid_unchanged = deepcopy(test_pixel_grid)
    recv_blobs = get_blobs(test_pixel_grid)
    expected_blobs = [
        BlobTuple(
            # Outer contour
            [(1,2), (1,3), (1,4), (2,4), (2,3), (2,2)],
            # Blob mask
            [
                [False, False, False, False, False],
                [False, False, True,  True,  False],
                [False, False, False, False, False],
            ],
            # Total mask
            [
                [False, False, False, False, False],
                [False, False, True,  True,  False],
                [False, False, False, False, False],
            ],
            # Sub-blobs
            [],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert test_pixel_grid == test_pixel_grid_unchanged


def test_get_blobs_two():
    test_pixel_grid = [
        [0, 1],
        [1, 0],
    ]
    test_pixel_grid_unchanged = deepcopy(test_pixel_grid)
    recv_blobs = get_blobs(test_pixel_grid)
    expected_blobs = [
        BlobTuple(
            # Outer contour
            [(0,1), (0,2), (1,2), (1,1)],
            # Blob mask
            [
                [False, True ],
                [False, False],
            ],
            # Total mask
            [
                [False, True ],
                [False, False],
            ],
            # Sub-blobs
            [],
        ),
        BlobTuple(
            # Outer contour
            [(1,0), (1,1), (2,1), (2,0)],
            # Blob mask
            [
                [False, False],
                [True,  False],
            ],
            # Total mask
            [
                [False, False],
                [True,  False],
            ],
            # Sub-blobs
            [],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert test_pixel_grid == test_pixel_grid_unchanged


def test_get_two_blobs_adjacent():
    test_pixel_grid = [
        [1, 2],
    ]
    test_pixel_grid_unchanged = deepcopy(test_pixel_grid)
    recv_blobs = get_blobs(test_pixel_grid)
    expected_blobs = [
        BlobTuple(
            # Outer contour
            [(0,0), (0,1), (1,1), (1,0)],
            # Blob mask
            [
                [True, False],
            ],
            # Total mask
            [
                [True, False],
            ],
            # Sub-blobs
            [],
        ),
        BlobTuple(
            # Outer contour
            [(0,1), (0,2), (1,2), (1,1)],
            # Blob mask
            [
                [False, True],
            ],
            # Total mask
            [
                [False, True],
            ],
            # Sub-blobs
            [],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert test_pixel_grid == test_pixel_grid_unchanged


def test_get_blobs_one_with_void():
    test_pixel_grid = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    test_pixel_grid_unchanged = deepcopy(test_pixel_grid)
    recv_blobs = get_blobs(test_pixel_grid)
    expected_blobs = [
        BlobTuple(
            # Outer contour
            [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0), (2,0), (1,0)],
            # Blob mask
            [
                [True,  True,  True],
                [True,  False, True],
                [True,  True,  True],
            ],
            # Total mask
            [
                [True,  True,  True],
                [True,  True,  True],
                [True,  True,  True],
            ],
            # Sub-blobs
            [],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert test_pixel_grid == test_pixel_grid_unchanged


def test_get_blobs_one_with_two_voids():
    test_pixel_grid = [
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
    ]
    test_pixel_grid_unchanged = deepcopy(test_pixel_grid)
    recv_blobs = get_blobs(test_pixel_grid)
    expected_blobs = [
        BlobTuple(
            # Outer contour
            [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,5), (2,5), (3,5), (3,4), (3,3), (3,2), (3,1), (3,0), (2,0), (1,0)],
            # Blob mask
            [
                [True,  True,  True,  True,  True],
                [True,  False, True,  False, True],
                [True,  True,  True,  True,  True],
            ],
            # Total mask
            [
                [True,  True,  True,  True,  True],
                [True,  True,  True,  True,  True],
                [True,  True,  True,  True,  True],
            ],
            # Sub-blobs
            [],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert test_pixel_grid == test_pixel_grid_unchanged


def test_get_blobs_nested():
    test_pixel_grid = [
        [1, 1, 1],
        [1, 2, 1],
        [1, 1, 1],
    ]
    test_pixel_grid_unchanged = deepcopy(test_pixel_grid)
    recv_blobs = get_blobs(test_pixel_grid)
    expected_blobs = [
        BlobTuple(
            # Outer contour
            [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0), (2,0), (1,0)],
            # Blob mask
            [
                [True,  True,  True],
                [True,  False, True],
                [True,  True,  True],
            ],
            # Total mask
            [
                [True,  True,  True],
                [True,  True,  True],
                [True,  True,  True],
            ],
            # Sub-blobs
            [
                BlobTuple(
                    # Outer contour
                    [(1,1), (1,2), (2,2), (2,1)],
                    # Blob mask
                    [
                        [False, False, False],
                        [False, True,  False],
                        [False, False, False],
                    ],
                    # Total mask
                    [
                        [False, False, False],
                        [False, True,  False],
                        [False, False, False],
                    ],
                    # Sub-blobs
                    [],
                ),
            ],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert test_pixel_grid == test_pixel_grid_unchanged



def test_get_blobs_nested_with_void_buffer():
    test_pixel_grid = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 2, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]
    test_pixel_grid_unchanged = deepcopy(test_pixel_grid)
    recv_blobs = get_blobs(test_pixel_grid)
    expected_blobs = [
        BlobTuple(
            # Outer contour
            [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,5), (2,5), (3,5), (4,5), (5,5), (5,4), (5,3), (5,2), (5,1), (5,0), (4,0), (3,0), (2,0), (1,0)],
            # Blob mask
            [
                [True,  True,  True,  True,  True],
                [True,  False, False, False, True],
                [True,  False, False, False, True],
                [True,  False, False, False, True],
                [True,  True,  True,  True,  True],
            ],
            # Total mask
            [
                [True,  True,  True,  True,  True],
                [True,  True,  True,  True,  True],
                [True,  True,  True,  True,  True],
                [True,  True,  True,  True,  True],
                [True,  True,  True,  True,  True],
            ],
            # Sub-blobs
            [
                BlobTuple(
                    # Outer contour
                    [(2,2), (2,3), (3,3), (3,2)],
                    # Blob mask
                    [
                        [False, False, False, False, False],
                        [False, False, False, False, False],
                        [False, False, True,  False, False],
                        [False, False, False, False, False],
                        [False, False, False, False, False],
                    ],
                    # Total mask
                    [
                        [False, False, False, False, False],
                        [False, False, False, False, False],
                        [False, False, True,  False, False],
                        [False, False, False, False, False],
                        [False, False, False, False, False],
                    ],
                    # Sub-blobs
                    [],
                ),
            ],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert test_pixel_grid == test_pixel_grid_unchanged


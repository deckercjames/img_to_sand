
from process_image import get_blobs
from process_image import BlobTuple
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
            # Blob mask
            [
                [False, False, False, False, False],
                [False, False, True,  True,  False],
                [False, False, False, False, False],
            ],
            # Outer contour
            [(1,2), (1,3), (1,4), (2,4), (2,3), (2,2)],
            # Void contours
            [],
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
            # Blob mask
            [
                [False, True ],
                [False, False],
            ],
            # Outer contour
            [(0,1), (0,2), (1,2), (1,1)],
            # Void contours
            [],
            # Sub-blobs
            [],
        ),
        BlobTuple(
            # Blob mask
            [
                [False, False],
                [True,  False],
            ],
            # Outer contour
            [(1,0), (1,1), (2,1), (2,0)],
            # Void contours
            [],
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
            # Blob mask
            [
                [True, False],
            ],
            # Outer contour
            [(0,0), (0,1), (1,1), (1,0)],
            # Void contours
            [],
            # Sub-blobs
            [],
        ),
        BlobTuple(
            # Blob mask
            [
                [False, True],
            ],
            # Outer contour
            [(0,1), (0,2), (1,2), (1,1)],
            # Void contours
            [],
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
            # Blob mask
            [
                [True,  True,  True],
                [True,  False, True],
                [True,  True,  True],
            ],
            # Outer contour
            [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0), (2,0), (1,0)],
            # Void contours
            [
                [(1,1), (1,2), (2,2), (2,1)],
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
            # Blob mask
            [
                [True,  True,  True,  True,  True],
                [True,  False, True,  False, True],
                [True,  True,  True,  True,  True],
            ],
            # Outer contour
            [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,5), (2,5), (3,5), (3,4), (3,3), (3,2), (3,1), (3,0), (2,0), (1,0)],
            # Void contours
            [
                [(1,1), (1,2), (2,2), (2,1)],
                [(1,3), (1,4), (2,4), (2,3)],
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
            # Blob mask
            [
                [True,  True,  True],
                [True,  False, True],
                [True,  True,  True],
            ],
            # Outer contour
            [(0,0), (0,1), (0,2), (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0), (2,0), (1,0)],
            # Void contours
            [
                [(1,1), (1,2), (2,2), (2,1)],
            ],
            # Sub-blobs
            [
                BlobTuple(
                    # Blob mask
                    [
                        [False, False, False],
                        [False, True,  False],
                        [False, False, False],
                    ],
                    # Outer contour
                    [(1,1), (1,2), (2,2), (2,1)],
                    # Void contours
                    [],
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
            # Blob mask
            [
                [True,  True,  True,  True,  True],
                [True,  False, False, False, True],
                [True,  False, False, False, True],
                [True,  False, False, False, True],
                [True,  True,  True,  True,  True],
            ],
            # Outer contour
            [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (1,5), (2,5), (3,5), (4,5), (5,5), (5,4), (5,3), (5,2), (5,1), (5,0), (4,0), (3,0), (2,0), (1,0)],
            # Void contours
            [
                [(1,1), (1,2), (1,3), (1,4), (2,4), (3,4), (4,4), (4,3), (4,2), (4,1), (3,1), (2,1)],
            ],
            # Sub-blobs
            [
                BlobTuple(
                    # Blob mask
                    [
                        [False, False, False, False, False],
                        [False, False, False, False, False],
                        [False, False, True,  False, False],
                        [False, False, False, False, False],
                        [False, False, False, False, False],
                    ],
                    # Outer contour
                    [(2,2), (2,3), (3,3), (3,2)],
                    # Void contours
                    [],
                    # Sub-blobs
                    [],
                ),
            ],
        ),
    ]
    assert len(recv_blobs) == len(expected_blobs)
    assert recv_blobs == expected_blobs
    assert test_pixel_grid == test_pixel_grid_unchanged


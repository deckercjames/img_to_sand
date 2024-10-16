
from src.linker.linkable_entity.linkable_entity_blob import LinkableEntityBlob
from src.linker.linkable_entity.linkable_entity_blob import get_blob_linkable_entity
from src.topography import get_all_blobs_from_mask

from testing.testing_helpers import helper_mask_string_to_bool_mask

from copy import deepcopy


def helper_get_mask_with_gateway_points_as_str(grid_mask, gateway_points):
    buf = ""
    for r, row in enumerate(grid_mask):
        for c, cell in enumerate(row):
            if (r,c) in gateway_points:
                buf += '#'
            elif cell:
                buf += '.'
            else:
                buf += ' '
        buf += "\n"
    return buf



def test_linkable_entity_blob_basic():
    test_grid_mask_str = [
        "              ",
        "  #########   ",
        " ###########  ",
        " ############ ",
        "  ########### ",
        "  ########### ",
        "   ####       ",
        "              ",
    ]
    test_grid_mask = helper_mask_string_to_bool_mask(test_grid_mask_str)
    exp_test_grid_mask_unchanged = deepcopy(test_grid_mask)
    test_blobs = get_all_blobs_from_mask(test_grid_mask)
    assert len(test_blobs) == 1
    # Test Function
    recv_linkable_entity = get_blob_linkable_entity(test_blobs[0])
    recv_entry_pts_str = helper_get_mask_with_gateway_points_as_str(test_grid_mask, recv_linkable_entity.get_entry_points())
    recv_exit_pts_str = helper_get_mask_with_gateway_points_as_str(test_grid_mask, recv_linkable_entity.get_exit_points())
    # Define Exected Output
    exp_entry_str_rep = \
        "              \n" \
        "  ##########  \n" \
        " ##........## \n" \
        " #..######..##\n" \
        " ##.######...#\n" \
        "  #..........#\n" \
        "  ##...#######\n" \
        "   #####      \n"
    exp_exit_str_rep = \
        "              \n" \
        "  ##########  \n" \
        " ##........## \n" \
        " #..........##\n" \
        " ##..........#\n" \
        "  #..........#\n" \
        "  ##...#######\n" \
        "   #####      \n"
    exp_end_points = [(3,19), (5,6)]
    # Assert
    print("RECEIVED ENTRY POINTS")
    print(recv_entry_pts_str)
    print("RECEIVED EXIT POINTS")
    print(recv_exit_pts_str)
    assert type(recv_linkable_entity) == LinkableEntityBlob
    assert recv_entry_pts_str == exp_entry_str_rep
    assert recv_exit_pts_str == exp_exit_str_rep
    assert recv_linkable_entity.get_entity_grid_mask() == exp_test_grid_mask_unchanged
    assert test_grid_mask == exp_test_grid_mask_unchanged


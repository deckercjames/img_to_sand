
from src.linker.linkable_entity.linkable_entity_line import LinkableEntityLine
from src.linker.linkable_entity.linkable_entity_line import get_line_linkable_entity

from testing.unit_tests.testing_helpers import helper_mask_string_to_numpy_bool_mask

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
        


def test_linkable_entity_line_basic():
    test_grid_mask_str = [
        "                     ",
        "  #########          ",
        " #         #####     ",
        " #              #### ",
        "  #                  ",
        "   ####              ",
        "                     ",
    ]
    test_grid_mask = helper_mask_string_to_numpy_bool_mask(test_grid_mask_str)
    exp_test_grid_mask_unchanged = deepcopy(test_grid_mask)
    recv_linkable_entity = get_line_linkable_entity(test_grid_mask) # spacing not used for this test
    exp_end_points = [(3,19), (5,6)]
    assert type(recv_linkable_entity) == LinkableEntityLine
    assert recv_linkable_entity.get_entry_points() == exp_end_points
    assert recv_linkable_entity.get_exit_points() == exp_end_points
    assert (recv_linkable_entity.get_entity_grid_mask() == exp_test_grid_mask_unchanged).all()
    assert (test_grid_mask == exp_test_grid_mask_unchanged).all()


# TODO These are kinda verifying the same thing now that the spacing optional has been removed
def test_linkable_entity_closed_loop():
    test_grid_mask_str = [
        "                  ",
        "  #########       ",
        " #         #####  ",
        " #              # ",
        "  #           ##  ",
        "   ####      #    ",
        "       ######     ",
        "                  ",
    ]
    test_grid_mask = helper_mask_string_to_numpy_bool_mask(test_grid_mask_str)
    exp_test_grid_mask_unchanged = deepcopy(test_grid_mask)
    recv_linkable_entity = get_line_linkable_entity(test_grid_mask)
    recv_entry_pts_str = helper_get_mask_with_gateway_points_as_str(test_grid_mask, recv_linkable_entity.get_entry_points())
    recv_exit_pts_str = helper_get_mask_with_gateway_points_as_str(test_grid_mask, recv_linkable_entity.get_exit_points())
    exp_end_str_rep = \
        "                  \n" \
        "  #########       \n" \
        " #         #####  \n" \
        " #              # \n" \
        "  #           ##  \n" \
        "   ####      #    \n" \
        "       ######     \n" \
        "                  \n"
    print("RECEIVED")
    print(recv_entry_pts_str)
    assert type(recv_linkable_entity) == LinkableEntityLine
    assert recv_entry_pts_str == exp_end_str_rep
    assert recv_exit_pts_str == exp_end_str_rep
    assert (recv_linkable_entity.get_entity_grid_mask() == exp_test_grid_mask_unchanged).all()
    assert (test_grid_mask == exp_test_grid_mask_unchanged).all()


def test_linkable_entity_closed_loops_at_border():
    test_grid_mask_str = [
        " ######## #      ",
        "#        # ##### ",
        "#        #      #",
        " ##      #    ## ",
        "   ####  #   #   ",
        "       ## ###    ",
    ]
    test_grid_mask = helper_mask_string_to_numpy_bool_mask(test_grid_mask_str)
    exp_test_grid_mask_unchanged = deepcopy(test_grid_mask)
    recv_linkable_entity = get_line_linkable_entity(test_grid_mask)
    recv_entry_pts_str = helper_get_mask_with_gateway_points_as_str(test_grid_mask, recv_linkable_entity.get_entry_points())
    recv_exit_pts_str = helper_get_mask_with_gateway_points_as_str(test_grid_mask, recv_linkable_entity.get_exit_points())
    exp_end_str_rep = \
        " ######## #      \n" \
        "#        # ##### \n" \
        "#        #      #\n" \
        " ##      #    ## \n" \
        "   ####  #   #   \n" \
        "       ## ###    \n"
    print("RECEIVED")
    print(recv_entry_pts_str)
    assert type(recv_linkable_entity) == LinkableEntityLine
    assert recv_entry_pts_str == exp_end_str_rep
    assert recv_exit_pts_str == exp_end_str_rep
    assert (recv_linkable_entity.get_entity_grid_mask() == exp_test_grid_mask_unchanged).all()
    assert (test_grid_mask == exp_test_grid_mask_unchanged).all()

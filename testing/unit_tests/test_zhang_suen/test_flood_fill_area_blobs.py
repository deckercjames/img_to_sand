
from src.linker.zhang_suen import get_flood_fill_area_blobs

from testing.unit_tests.testing_helpers import helper_mask_string_to_numpy_bool_mask
from testing.unit_tests.testing_helpers import helper_grid_mask_to_string


def test_get_area_blobs():
    orig_grid_mask_str = [
        "                                     ",
        "                          ######     ",
        "    ##########          #########    ",
        "   #         #####     ##########    ",
        "   #              ###############    ",
        "    #                 ###########    ",
        "     ####                #######     ",
        "                                     ",
    ]
    orig_test_mask = helper_mask_string_to_numpy_bool_mask(orig_grid_mask_str)
    micro_blob_test_mask_str = [
        "                                     ",
        "                                     ",
        "                                     ",
        "                            ##       ",
        "                            ##       ",
        "                            ##       ",
        "                                     ",
        "                                     ",
    ]
    micro_blob_test_mask = helper_mask_string_to_numpy_bool_mask(micro_blob_test_mask_str)
    
    result = get_flood_fill_area_blobs(orig_test_mask, micro_blob_test_mask, 9)
    
    result_str = helper_grid_mask_to_string(result)
    exp_result = \
        "                                     \n" \
        "                          ######     \n" \
        "                        #########    \n" \
        "                       ##########    \n" \
        "                   ##############    \n" \
        "                      ###########    \n" \
        "                         #######     \n" \
        "                                     \n"
    print("EXPECTED")
    print(exp_result)
    print("RECEIVED")
    print(result_str)
    assert result_str == exp_result

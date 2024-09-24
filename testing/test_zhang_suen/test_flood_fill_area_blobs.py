
from src.zhang_suen import get_flood_fill_area_blobs


def helper_mask_string_to_bool_mask(str_rep):
    result = []
    for row in str_rep:
        result.append([c == "#" for c in row])
    return result

def helper_grid_mask_to_string(grid_mask):
    buf = ""
    for row in grid_mask:
        for cell in row:
            buf += "#" if cell else " "
        buf += "\n"
    return buf


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
    orig_test_mask = helper_mask_string_to_bool_mask(orig_grid_mask_str)
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
    micro_blob_test_mask = helper_mask_string_to_bool_mask(micro_blob_test_mask_str)
    
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

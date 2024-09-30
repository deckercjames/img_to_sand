
from src.zhang_suen import get_split_lines_and_blobs

from testing.testing_helpers import helper_mask_string_to_bool_mask
from testing.testing_helpers import helper_grid_mask_to_string



def test_zhang_suen_basic():
    test_mask_str = [
        "                          #######    ",
        "   ###########           ##########  ",
        "  #############         ###########  ",
        " ####       ######     ############  ",
        " ####        ######################  ",
        "  ####                #############  ",
        "   ######                ########    ",
        "      #####                          ",
    ]
    test_mask = helper_mask_string_to_bool_mask(test_mask_str)
    
    result_blob, result_line = get_split_lines_and_blobs(test_mask, 2)
    
    result_blob_str = helper_grid_mask_to_string(result_blob)
    result_line_str = helper_grid_mask_to_string(result_line)

    exp_result_blob = \
        "                          #######    \n" \
        "                         ##########  \n" \
        "                        ###########  \n" \
        "                       ############  \n" \
        "                      #############  \n" \
        "                      #############  \n" \
        "                         ########    \n" \
        "                                     \n"

    exp_result_line = \
        "                                     \n" \
        "    #########                        \n" \
        "   ##       ##                       \n" \
        "   #         ####                    \n" \
        "   #             #####               \n" \
        "   ##                                \n" \
        "     ###                             \n" \
        "        ###                          \n"

    print("EXPECTED BLOB")
    print(exp_result_blob)
    print("EXPECTED LINE")
    print(exp_result_line)
    print("RECEIVED BLOB")
    print(result_blob_str)
    print("RECEIVED LINE")
    print(result_line_str)
    assert result_blob_str == exp_result_blob
    assert result_line_str == exp_result_line



def test_zhang_suen_two_double_connected_blobs():
    test_mask_str = [
        "       #############         ###############",
        "   ###################    ##################",
        "   #############   ##############        ## ",
        "   #############      ########         ##   ",
        "    ############                      ###   ",
        " ###############               #######      ",
        "   #############              ##########    ",
        "      ########               ###########    ",
        "       ####                 ############    ",
        "       ####      ########################## ",
        "       ###############       #############  ",
        "         ########              ########     ",
    ]
    test_mask = helper_mask_string_to_bool_mask(test_mask_str)
    
    result_blob, result_line = get_split_lines_and_blobs(test_mask, 2)
    
    result_blob_str = helper_grid_mask_to_string(result_blob)
    result_line_str = helper_grid_mask_to_string(result_line)

    exp_result_blob = \
        "       ############                         \n" \
        "   ################                         \n" \
        "   #############                            \n" \
        "   #############                       ##   \n" \
        "    ############                      ###   \n" \
        " ###############               #######      \n" \
        "   #############              ##########    \n" \
        "      ########               ###########    \n" \
        "       ####                 ############    \n" \
        "       ####                 ############### \n" \
        "       #####                 #############  \n" \
        "                               ########     \n"

    exp_result_line = \
        "                                ##########  \n" \
        "                   ##        ###         #  \n" \
        "                     ########            #  \n" \
        "                                            \n" \
        "                                            \n" \
        "                                            \n" \
        "                                            \n" \
        "                                            \n" \
        "                                            \n" \
        "                  ##########                \n" \
        "            ######                          \n" \
        "                                            \n"

    print("EXPECTED BLOB")
    print(exp_result_blob)
    print("EXPECTED LINE")
    print(exp_result_line)
    print("RECEIVED BLOB")
    print(result_blob_str)
    print("RECEIVED LINE")
    print(result_line_str)
    assert result_blob_str == exp_result_blob
    assert result_line_str == exp_result_line



# def test_zhang_suen_zero_itterations():
#     test_mask_str = [
#         "         ",
#         " ######  ",
#         "   ####  ",
#         " ####### ",
#         "         ",
#     ]
#     test_mask = helper_mask_string_to_bool_mask(test_mask_str)
    
#     result_blob, result_line = get_split_lines_and_blobs(test_mask, 0)
    
#     result_blob_str = helper_grid_mask_to_string(result_blob)
#     result_line_str = helper_grid_mask_to_string(result_line)

#     exp_result_blob = \
#         "         \n" \
#         " ######  \n" \
#         "   ####  \n" \
#         " ####### \n" \
#         "         \n" \

#     exp_result_line = \
#         "         \n" \
#         "         \n" \
#         "         \n" \
#         "         \n" \
#         "         \n" \

#     print("EXPECTED BLOB")
#     print(exp_result_blob)
#     print("EXPECTED LINE")
#     print(exp_result_line)
#     print("RECEIVED BLOB")
#     print(result_blob_str)
#     print("RECEIVED LINE")
#     print(result_line_str)
#     assert result_blob_str == exp_result_blob
#     assert result_line_str == exp_result_line

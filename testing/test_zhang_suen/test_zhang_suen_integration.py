
from src.zhang_suen import get_split_lines_and_blobs

from testing.testing_helpers import helper_mask_string_to_bool_mask
from testing.testing_helpers import helper_grid_mask_to_string
from testing.testing_helpers import helper_pretty_mask_compare



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
    
    exp_result_blob = [
        "                          #######    ",
        "                         ##########  ",
        "                        ###########  ",
        "                       ############  ",
        "                      #############  ",
        "                      #############  ",
        "                         ########    ",
        "                                     ",
    ]

    exp_result_line = [
        "                                     ",
        "    #########                        ",
        "   ##       ##                       ",
        "   #         ####                    ",
        "   #             #####               ",
        "   ##                                ",
        "     ###                             ",
        "        ###                          ",
    ]
    assert helper_pretty_mask_compare(exp_result_line, result_line)
    assert helper_pretty_mask_compare(exp_result_blob, result_blob)



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
    
    exp_result_blob = [
        "       ############                         ",
        "   ################                         ",
        "   #############                            ",
        "   #############                       ##   ",
        "    ############                      ###   ",
        " ###############               #######      ",
        "   #############              ##########    ",
        "      ########               ###########    ",
        "       ####                 ############    ",
        "       ####                 ############### ",
        "       #####                 #############  ",
        "                               ########     ",
    ]

    exp_result_line = [
        "                                ##########  ",
        "                   ##        ###         #  ",
        "                     ########            #  ",
        "                                            ",
        "                                            ",
        "                                            ",
        "                                            ",
        "                                            ",
        "                                            ",
        "                  ##########                ",
        "            ######                          ",
        "                                            ",
    ]

    assert helper_pretty_mask_compare(exp_result_line, result_line)
    assert helper_pretty_mask_compare(exp_result_blob, result_blob)



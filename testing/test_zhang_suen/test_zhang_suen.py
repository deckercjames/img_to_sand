
from src.zhang_suen import zhang_suen_errosion
from src.zhang_suen import zhang_suen_errosion_itteration

from testing.testing_helpers import helper_mask_string_to_bool_mask
from testing.testing_helpers import helper_grid_mask_to_string

def test_zhang_suen_basic():
    test_mask_str = [
        "#################                   #############       ",
        "##################               ################       ",
        "###################            ##################       ",
        "########     #######          ###################       ",
        "  ######     #######         #######       ######       ",
        "  ######     #######        #######                     ",
        "  #################         #######                     ",
        "  ################          #######                     ",
        "  #################         #######                     ",
        "  ######     #######        #######                     ",
        "  ######     #######        #######                     ",
        "  ######     #######         #######       ######       ",
        "########     #######          ###################       ",
        "########     ####### ######    ################## ######",
        "########     ####### ######      ################ ######",
        "########     ####### ######         ############# ######",
    ]
    test_mask = helper_mask_string_to_bool_mask(test_mask_str)
    result = zhang_suen_errosion(test_mask)
    result_str = helper_grid_mask_to_string(result)
    exp_result = \
        "                                                        \n" \
        "   # ##########                       #######           \n" \
        "    ##        #                   ####       #          \n" \
        "    #          #                 ##                     \n" \
        "    #          #                #                       \n" \
        "    #          #                #                       \n" \
        "    #          #                #                       \n" \
        "    ############               #                        \n" \
        "    #          #               #                        \n" \
        "    #          #                #                       \n" \
        "    #          #                #                       \n" \
        "    #          #                #                       \n" \
        "    #                            ##                     \n" \
        "    #                             ############          \n" \
        "                      ###                          ###  \n" \
        "                                                        \n"
    assert result_str == exp_result

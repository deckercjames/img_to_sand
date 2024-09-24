
from src.zhang_suen import zhang_suen_errosion
from src.zhang_suen import zhang_suen_errosion_itteration

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

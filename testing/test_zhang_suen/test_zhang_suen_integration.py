
from src.zhang_suen import get_split_lines_and_blobs

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

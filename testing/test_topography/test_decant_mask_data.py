
from src.topography import decant_mask_data_from_topography_tree
from src.tree import TreeNode
from src.blob_extraction import Blob


def test_decant_basic():
    test_tree = TreeNode(
        Blob(
            [(0,0), (0,1), (1,1), (1,0)],
            [
                [True ],
            ],
            [
                [True ],
            ],
        ),
        children=[]
    )
    exp_tree = TreeNode(
        [(0,0), (0,1), (1,1), (1,0)],
        children=[]
    )
    rc = decant_mask_data_from_topography_tree(test_tree)
    assert rc is None
    assert test_tree == exp_tree

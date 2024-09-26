
from src.tree import TreeNode
from src.tree import unwrap_tree_post_order_traversal


def test_post_ord_trav_basic():
    test_tree = TreeNode(
        1,
        [
            TreeNode(
                2,
                [
                    TreeNode(
                        3,
                    ),
                    TreeNode(
                        4
                    )
                ]
            ),
            TreeNode(
                5
            )
        ]
    )
    expected_order = [3, 4, 2, 5, 1]
    recv_order = unwrap_tree_post_order_traversal(test_tree)
    assert recv_order == expected_order
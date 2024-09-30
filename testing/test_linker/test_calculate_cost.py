
from src.linker.linker import calculate_cost
from src.linker.linker import LinkerProblem
from src.linker.linker import CostMenu
from src.linker.linker import LinkerSearchState


def test_calc_cost_basic():
    test_problem = LinkerProblem(
        layers=None, # Not used by the tested function
        total_image_mask=[
            [False, True,  True,  True,  False]
        ],
        num_rows=5,
        num_cols=6,
        cost_menu=CostMenu(
            visited_mask_cost=100000,
            future_mask_cost=0,
            base_cost=1
        )
    )
    test_state = LinkerSearchState(
        cur_entity_ref=None, # Not used by the tested function
        visited_mask=[
            [False, False, False, True, True]
        ],
        visited_layer_entity_idx_set=None, # Not used by the tested function
        cost_to_state=None, # Not used by the tested function
        path=None # Not used by the tested function
    )
    test_p0 = (0, 0)
    test_p1 = (0, 5)
    recv_cost = calculate_cost(test_problem, test_state, test_p0, test_p1)
    exp_cost = (2 * 100000) + (2 * 0) + (2 * 1)
    assert recv_cost == exp_cost
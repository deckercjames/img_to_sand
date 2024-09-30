

from src.linker.linker import get_entity_link_with_border
from src.linker.linker import LinkerProblem



def test_get_entity_link_with_border_north():
    test_problem = LinkerProblem(
        layers=None, # Not used for the tested function
        total_image_mask=None, # Not used for the tested function
        num_rows=10,
        num_cols=12,
        cost_menu=None, # Not used for the tested function
    )
    test_conn_points = [
        (3,3),
        (3,4),
        (3,5),
        (2,5),
        (2,6),
        (3,6),
        (4,6),
    ]
    entity_pt, border_pt = get_entity_link_with_border(test_problem, test_conn_points)
    assert entity_pt == (2,5)
    assert border_pt == (0,5)


def test_get_entity_link_with_border_south():
    test_problem = LinkerProblem(
        layers=None, # Not used for the tested function
        total_image_mask=None, # Not used for the tested function
        num_rows=7,
        num_cols=12,
        cost_menu=None, # Not used for the tested function
    )
    test_conn_points = [
        (3,3),
        (3,4),
        (3,5),
        (2,5),
        (2,6),
        (3,6),
        (4,6),
        (5,6),
        (6,6),
        (6,5),
        (6,4),
    ]
    entity_pt, border_pt = get_entity_link_with_border(test_problem, test_conn_points)
    assert entity_pt == (6,6)
    assert border_pt == (7,6)


def test_get_entity_link_with_border_east():
    test_problem = LinkerProblem(
        layers=None, # Not used for the tested function
        total_image_mask=None, # Not used for the tested function
        num_rows=7,
        num_cols=5,
        cost_menu=None, # Not used for the tested function
    )
    test_conn_points = [
        (3,3),
        (3,4),
        (4,4),
        (4,3),
        (4,2),
        (3,2),
    ]
    entity_pt, border_pt = get_entity_link_with_border(test_problem, test_conn_points)
    assert entity_pt == (3,4)
    assert border_pt == (3,5)


def test_get_entity_link_with_border_west():
    test_problem = LinkerProblem(
        layers=None, # Not used for the tested function
        total_image_mask=None, # Not used for the tested function
        num_rows=7,
        num_cols=12,
        cost_menu=None, # Not used for the tested function
    )
    test_conn_points = [
        (3,3),
        (3,4),
        (4,4),
        (4,3),
        (4,2),
        (3,2),
    ]
    entity_pt, border_pt = get_entity_link_with_border(test_problem, test_conn_points)
    assert entity_pt == (4,2)
    assert border_pt == (4,0)


def test_get_entity_link_with_border_north_touching():
    test_problem = LinkerProblem(
        layers=None, # Not used for the tested function
        total_image_mask=None, # Not used for the tested function
        num_rows=10,
        num_cols=12,
        cost_menu=None, # Not used for the tested function
    )
    test_conn_points = [
        (0,3),
        (0,4),
        (1,4),
        (1,3),
    ]
    entity_pt, border_pt = get_entity_link_with_border(test_problem, test_conn_points)
    assert entity_pt == (0,3)
    assert border_pt == (0,3)


def test_get_entity_link_with_border_south_touching():
    test_problem = LinkerProblem(
        layers=None, # Not used for the tested function
        total_image_mask=None, # Not used for the tested function
        num_rows=4,
        num_cols=12,
        cost_menu=None, # Not used for the tested function
    )
    test_conn_points = [
        (3,3),
        (3,4),
        (4,4),
        (4,3),
    ]
    entity_pt, border_pt = get_entity_link_with_border(test_problem, test_conn_points)
    assert entity_pt == (4,4)
    assert border_pt == (4,4)

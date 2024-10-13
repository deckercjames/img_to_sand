

from src.path_elaboration.elaborator import elaborate_border



def test_border_elaborate_same_side():
    # North border
    recv_path = elaborate_border(5, 9, (0,2),  (0,7))
    assert recv_path == []
    recv_path = elaborate_border(5, 9, (0,7),  (0,2))
    assert recv_path == []
    # South border
    recv_path = elaborate_border(5, 9, (5,2),  (5,7))
    assert recv_path == []
    recv_path = elaborate_border(5, 9, (5,7),  (5,2))
    assert recv_path == []
    # East border
    recv_path = elaborate_border(5, 9, (2,9),  (4,9))
    assert recv_path == []
    recv_path = elaborate_border(5, 9, (4,9),  (2,9))
    assert recv_path == []
    # West border
    recv_path = elaborate_border(5, 9, (2,0),  (4,0))
    assert recv_path == []
    recv_path = elaborate_border(5, 9, (4,0),  (2,0))
    assert recv_path == []
    

def test_border_elaborate_one_turn():
    # North-West corner
    recv_path = elaborate_border(5, 9, (0,2),  (2,0))
    assert recv_path == [(0,0)]
    recv_path = elaborate_border(5, 9, (2,0),  (0,2))
    assert recv_path == [(0,0)]
    # North-East corner
    recv_path = elaborate_border(5, 9, (0,7),  (2,9))
    assert recv_path == [(0,9)]
    recv_path = elaborate_border(5, 9, (2,9),  (0,7))
    assert recv_path == [(0,9)]
    # South-East corner
    recv_path = elaborate_border(5, 9, (3,9),  (5,7))
    assert recv_path == [(5,9)]
    recv_path = elaborate_border(5, 9, (5,7),  (3,9))
    assert recv_path == [(5,9)]
    # South-West corner
    recv_path = elaborate_border(5, 9, (3,0),  (5,3))
    assert recv_path == [(5,0)]
    recv_path = elaborate_border(5, 9, (5,3),  (3,0))
    assert recv_path == [(5,0)]


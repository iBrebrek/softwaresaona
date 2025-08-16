import pytest

from saona.road_map import Direction, RoadMap


def test_direction():
    assert len(set(Direction.get_all())) == 4
    assert Direction.LEFT.opposite is Direction.RIGHT
    assert Direction.RIGHT.opposite is Direction.LEFT
    assert Direction.UP.opposite is Direction.DOWN
    assert Direction.DOWN.opposite is Direction.UP

    assert Direction.LEFT.next_position((5, 5)) == (5, 4)
    assert Direction.RIGHT.next_position((5, 5)) == (5, 6)
    assert Direction.UP.next_position((5, 5)) == (4, 5)
    assert Direction.DOWN.next_position((5, 5)) == (6, 5)


def test_road_map():
    map_ = RoadMap(
        [
            ["@", "+", ""],
            ["", "+", "-", "-", "x"],
        ],
        (0, 0),
    )

    assert map_.position == (0, 0)
    # cannot move to a cell without a road
    with pytest.raises(ValueError):
        map_.move(Direction.LEFT)
    with pytest.raises(ValueError):
        map_.move(Direction.DOWN)
    with pytest.raises(ValueError):
        map_.jump_to((0, 2))

    # we can lookup any position
    assert map_[1, 4] == "x"
    # there is never Index error, only unusable cells
    assert map_[100, 100] == ""

    # cell becomes visited the first time we move there
    assert not map_.is_visited((0, 1))
    char = map_.move(Direction.RIGHT)
    assert char == "+"
    assert map_.is_visited((0, 1))

    # peek usuable cells that are next to the current one
    around = list(map_.iter_surroundings())
    assert len(around) == 2
    assert (Direction.LEFT, (0, 0)) in around
    assert (Direction.DOWN, (1, 1)) in around

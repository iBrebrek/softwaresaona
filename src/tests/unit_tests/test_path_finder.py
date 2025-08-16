from saona.road_map import RoadMap
from saona.path_finder import LetterCollector, PathFinder


def test_letter_collector():
    collector = LetterCollector()
    collector.collect((0, 0), "A")
    collector.collect((0, 0), "A")
    collector.collect((0, 1), "C")
    collector.collect((0, 0), "A")
    collector.collect((0, 1), "C")
    collector.collect((0, 0), "A")
    collector.collect((0, 2), "B")
    assert collector.get() == "ACB"


def test_path_finder():
    road_map = RoadMap(
        [
            ["@", "-", "A"],
            ["", "+", "+"],
            ["", "x", ""],
        ],
        (0, 0),
    )
    letters, path = PathFinder().follow_path(road_map)
    assert letters == "A"
    assert path == "@-A++x"

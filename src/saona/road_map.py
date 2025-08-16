from typing import Iterable
from enum import Enum


class Direction(Enum):
    """Enumeration used to represent directions when navigating `RoadMap`."""

    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4

    @property
    def opposite(self):
        """What would be a direction if we turn 180."""
        match self:
            case Direction.LEFT:
                return Direction.RIGHT
            case Direction.UP:
                return Direction.DOWN
            case Direction.RIGHT:
                return Direction.LEFT
            case Direction.DOWN:
                return Direction.UP

    @staticmethod
    def get_all():
        """Tuple of all four directions."""
        return (Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN)

    def next_position(self, position: tuple[int, int]):
        """Calculate a new position based on a direction.

        New position is an old position moved by one in the current direction.
        """
        row_idx, col_idx = position
        match self:
            case Direction.LEFT:
                col_idx -= 1
            case Direction.UP:
                row_idx -= 1
            case Direction.RIGHT:
                col_idx += 1
            case Direction.DOWN:
                row_idx += 1
        return row_idx, col_idx


class RoadMap:
    """Object used to navigate a readonly 2D array of characters.

    Use attribute `position` to get the current position.
    Use `your_road_map_obj[any_position]` to retrieve what is at the position.
    Cell either holds a character or an empty string.
    An empty string means that cell is unusable.
    Note that retrieval will never raise an error, even if position is out of bounds.
    To simplify `RoadMap` usage, all invalid positions are treated as unusable cells.

    To change the position, use methods `move` or `jump_to`.
    `RoadMap` tracks visited positions, use method `is_visited` to check if position was visited.

    Method `iter_surroundings` offers a way to see usable cells around the current position.

    Note that `RoadMap` doesn't know anything about used characters.
    Either cell has a character which means that cell is usable, or cell is unusable.
    """

    def __init__(self, grid: list[list[str]], initial_position: tuple[int, int]):
        self._grid = grid
        self.position = initial_position
        self._visited = [[False] * len(row) for row in grid]

    def jump_to(self, position: tuple[int, int]) -> str:
        """Go to any usuable cell."""
        char = self[position]
        if not char:
            raise ValueError("Position cannot be set to an unusable cell")
        self.position = position
        self._visited[position[0]][position[1]] = True
        return char

    def move(self, direction: Direction) -> str:
        """Move by one to an usuable cell in a direction."""
        next_position = direction.next_position(self.position)
        return self.jump_to(next_position)

    def is_visited(self, position: tuple[int, int]):
        """Check if position was ever visited."""
        try:
            return self._visited[position[0]][position[1]]
        except IndexError:
            return False

    def iter_surroundings(self) -> Iterable[tuple[Direction, tuple[int, int]]]:
        """Iterate over all usable surrounding cells.

        Checks all four directions around the current position.
        """
        for direction in Direction.get_all():
            position = direction.next_position(self.position)
            if not self[position]:
                continue
            yield direction, position

    def __getitem__(self, position: tuple[int, int]):
        """Retrieve a charater at the position.

        If cell is unusable empty string is returned.
        """
        if position[0] < 0 or position[1] < 0:
            return ""
        try:
            return self._grid[position[0]][position[1]]
        except IndexError:
            return ""

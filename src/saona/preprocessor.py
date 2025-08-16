from saona.util import END, HORIZONTAL, START, TURN, VERTICAL, PathError

__all__ = ("process",)

_VALID_SIGNS = (START, END, TURN, HORIZONTAL, VERTICAL, " ")


def process(grid_str: str) -> tuple[list[list[str]], tuple[int, int]]:
    """Process user input and get usable grid and starting position.

    Performs validations:
        - raises error if there is at least 1 unsupported charater
        - raises error if there is 0 or multiple starts
        - raises error if there is 0 or multiple ends
    Performs transformations:
        - splits string into 2D array of characters
        - sets unused cells to empty string
    """
    grid = [list(row) for row in grid_str.split("\n")]
    _adjust_grid(grid)
    start_idx = _find_start(grid)
    return grid, start_idx


def _is_letter(char: str):
    return char.isalpha() and char.isupper()


def _adjust_grid(grid: list[list[str]]):
    for row in grid:
        for col_idx, char in enumerate(row):
            if char not in _VALID_SIGNS and not _is_letter(char):
                raise PathError(f"There is an invalid character: {char}")
            if char == " ":
                # Simpler to use '' instead of ' ' for unusable cells
                row[col_idx] = ""


def _find_start(grid: list[list[str]]) -> tuple[int, int]:
    start = None
    has_end = False
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char == START:
                if start:
                    raise PathError("Map should have exactly one start")
                start = (row_idx, col_idx)
            elif char == END:
                if has_end:
                    raise PathError("Map should have exactly one end")
                has_end = True
    if not start:
        raise PathError("Map is missing a start")
    if not has_end:
        raise PathError("Map is missing an end")
    return start

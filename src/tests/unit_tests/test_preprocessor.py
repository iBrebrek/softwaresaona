import pytest

from saona.preprocessor import process
from saona.util import PathError


def test_transformation():
    grid, start = process("@-x")
    assert start == (0, 0)
    assert grid == [["@", "-", "x"]]

    grid, start = process(" x\n A@")
    assert start == (1, 2)
    # space became empty string
    assert grid == [["", "x"], ["", "A", "@"]]


def test_validation():
    # no start/end
    with pytest.raises(PathError):
        process("-x")
    with pytest.raises(PathError):
        process("@-")
    # more starts/ends
    with pytest.raises(PathError):
        process("@-x-@")
    with pytest.raises(PathError):
        process("@-x-x")
    with pytest.raises(PathError):
        process("@-x\n@-x")

    # unsupported characters
    with pytest.raises(PathError):
        process("@_x")

    # letters must be UPPER case
    with pytest.raises(PathError):
        process("@-a-x")
    grid, _ = process("@-A-Z-x")
    assert grid == [["@", "-", "A", "-", "Z", "-", "x"]]

    # support non-ASCII
    grid, _ = process("@-Š-x")
    assert grid == [["@", "-", "Š", "-", "x"]]

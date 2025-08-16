import pytest

from saona.main import traverse
from saona.util import PathError


# This test file uses all and only examples provided by Saona


def test_basic():
    letters, path = traverse("""
  @---A---+
          |
  x-B-+   C
      |   |
      +---+
""")
    assert letters == "ACB"
    assert path == "@---A---+|C|+---+|+-B-x"


def test_straight_through_intersections():
    letters, path = traverse("""
  @
  | +-C--+
  A |    |
  +---B--+
    |      x
    |      |
    +---D--+
""")
    assert letters == "ABCD"
    assert path == "@|A+---B--+|+--C-+|-||+---D--+|x"


def test_letters_on_turns():
    letters, path = traverse("""
  @---A---+
          |
  x-B-+   |
      |   |
      +---C
""")
    assert letters == "ACB"
    assert path == "@---A---+|||C---+|+-B-x"


def test_collected_letter_once():
    letters, path = traverse("""
     +-O-N-+
     |     |
     |   +-I-+
 @-G-O-+ | | |
     | | +-+ E
     +-+     S
             |
             x
""")
    assert letters == "GOONIES"
    assert path == "@-G-O-+|+-+|O||+-O-N-+|I|+-+|+-I-+|ES|x"


def test_compact_space():
    letters, path = traverse("""
 +-L-+
 |  +A-+
@B+ ++ H
 ++    x
""")
    assert letters == "BLAH"
    assert path == "@B+++B|+-L-+A+++A-+Hx"


def test_ignore_path_after_end():
    letters, path = traverse("""
  @-A--+
       |
       +-B--x-C--D
""")
    assert letters == "AB"
    assert path == "@-A--+|+-B--x"


def test_missing_start():
    grid = """
     -A---+
          |
  x-B-+   C
      |   |
      +---+
"""
    with pytest.raises(PathError):
        traverse(grid)


def test_missing_end():
    grid = """
   @--A---+
          |
    B-+   C
      |   |
      +---+
"""
    with pytest.raises(PathError):
        traverse(grid)


def test_multiple_starts():
    grid = """
   @--A-@-+
          |
  x-B-+   C
      |   |
      +---+
"""
    with pytest.raises(PathError):
        traverse(grid)

    grid = """
   @--A---+
          |
          C
          x
      @-B-+
"""
    with pytest.raises(PathError):
        traverse(grid)
    grid = """
   @--A--x

  x-B-+
      |
      @
"""
    with pytest.raises(PathError):
        traverse(grid)


def test_fork():
    grid = """
        x-B
          |
   @--A---+
          |
     x+   C
      |   |
      +---+
"""
    with pytest.raises(PathError):
        traverse(grid)


def test_broken_path():
    grid = """
   @--A-+
        |
         
        B-x
"""
    with pytest.raises(PathError):
        traverse(grid)


def test_multiple_starting_paths():
    with pytest.raises(PathError):
        traverse("x-B-@-A-x")


def test_fake_turn():
    with pytest.raises(PathError):
        traverse("@-A-+-B-x")

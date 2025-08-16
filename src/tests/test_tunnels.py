import pytest

from saona.main import traverse
from saona.util import PathError


def test_horizontal_tunnel():
    letters, path = traverse("""
  @
x-|-+
  +-A
""")
    assert letters == "A"
    assert path == "@|+-A+-|-x"


def test_vertical_tunnel():
    letters, path = traverse("""
    x
    |
  @---+
    | |
    +-+
""")
    assert letters == ""
    assert path == "@---+|+-+|-|x"


def test_turns_around_tunnel():
    letters, path = traverse("""
    +C-x
   @-A+
    +B+
""")
    assert letters == "ABC"
    assert path == "@-A++B+-+C-x"

    letters, path = traverse("""
    C-x
   @-A
    B+
""")
    assert letters == "ABC"
    assert path == "@-A+B-C-x"


def test_multiple_tunnels():
    letters, path = traverse("""
    C-B
 x--|-|F
  @---A|
    D--E
""")
    assert letters == "ABCDEF"
    assert path == "@---A|B-C|-D--E|F|-|--x"


def test_large_tunnel():
    letters, path = traverse("""
      H---------+
 @-------A      |
   C-----B      |
   D--E-----F   |
      +-----G   |
     ++         |
     +----------+
      |
      x
""")
    assert letters == "ABCDEFGH"
    assert (
        path
        == "@-------AB-----CD--E-----FG-----++++----------+|||||+---------H--E++-|x"
    )


def test_invalid_tunnels():
    grid = """
  +-+
  | |
@---+
  ----x
"""
    with pytest.raises(PathError):
        traverse(grid)

    # similar to test_large_tunnel, but tunnel has a hole
    grid = """
      H---------+
 @-------A      |
   C-----B      |
   D--E-----F   |
            |   |
      +-----G   |
     ++         |
     +----------+
      |
      x
"""
    with pytest.raises(PathError):
        traverse(grid)


def test_not_tunnel():
    # create tunnel for -|-
    letters, path = traverse("""                        
+---+
@ +-|--x
  +-+
""")
    assert letters == ""
    assert path == "@+---+|+-++-|--x"
    # avoid a tunnel for -|-
    with pytest.raises(PathError):
        traverse("@--|--x")


def test_tunnel_priority():
    letters, path = traverse("""
   A+
@--+|-x
   B+
""")
    assert letters == "AB"
    assert path == "@--+A+|+B+|-x"

from saona.main import traverse


def test_joined_fork():
    letters, path = traverse("""
  +-A-+
@-+   +-C-x
  +-B-+
""")
    # BAC is just as valid, depends on direction iteration
    assert letters == "ABC"
    assert path == "@-++-A-+++-B-+++-A-++-C-x"


def test_possible_detour():
    # Letters don't have to turn, but A could turn here.
    # Specification states "Keep direction, even in a compact space"
    # so it seems that going straight is the correct approach.
    letters, path = traverse("""
@--AZ-x
   +Y                        
""")
    assert letters == "AZ"
    assert path == "@--AZ-x"

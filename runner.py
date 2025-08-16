import sys

try:
    import saona
except ImportError:
    import os.path

    # Project is using uv, so simply using `uv run runner.py` will auto prepare env.
    # But if user wants to use `python runner.py` we should support it too.
    proj_root = os.path.dirname(__name__)
    sys.path.append(os.path.join(proj_root, "src"))
    import saona
import saona.util


def main():
    if len(sys.argv) < 2:
        print("Pass grid as an string argument")
    grid = sys.argv[1]
    print(grid)
    try:
        letters, path = saona.traverse(grid)
    except saona.util.PathError as e:
        print(f"Failed to follow the path: {e}")
    else:
        print(f"Collected letters: {letters}")
        print(f"Path followed: {path}")


if __name__ == "__main__":
    main()

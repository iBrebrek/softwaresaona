import saona.preprocessor
import saona.road_map
import saona.path_finder


def traverse(grid_str: str) -> tuple[str, str]:
    grid, initial_position = saona.preprocessor.process(grid_str)
    road_map = saona.road_map.RoadMap(grid, initial_position)
    path_finder = saona.path_finder.PathFinder()
    return path_finder.follow_path(road_map)

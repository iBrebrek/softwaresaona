from saona.road_map import Direction, RoadMap
from saona.util import END, HORIZONTAL, START, TURN, VERTICAL, PathError


class LetterCollector:
    """Collection used to track visited letters."""

    def __init__(self):
        self._letters = []
        self._positions = set()

    def collect(self, position: tuple[int, int], letter: str):
        if position not in self._positions:
            self._positions.add(position)
            self._letters.append(letter)

    def get(self) -> str:
        return "".join(self._letters)


class PathFinder:
    """Object used to follow a path."""

    def follow_path(self, road_map: RoadMap) -> tuple[str, str]:
        """Use provided road map to follow a path.

        If path can be succesfully followed till the end,
        `follow_path` returns collected letters and path taken.

        If it is impossible to reach the end, `PathError` is raised.
        """
        self._initialize(road_map)
        while True:
            char = self._map.move(self._direction)
            self._path.append(char)
            if char == END:
                path = "".join(self._path)
                return self._letters.get(), path

            if char.isalpha():
                self._letters.collect(self._map.position, char)
            self._analyze_next_move()

    def _initialize(self, road_map: RoadMap):
        assert road_map[road_map.position] == START
        self._path = [START]
        self._possible_inifinite_loops = set()
        self._map = road_map
        self._letters = LetterCollector()

        initial_direction = None
        for direction, position in self._map.iter_surroundings():
            char = self._map[position]
            if not self._char_supports_direction(char, direction):
                continue
            if initial_direction is not None:
                raise PathError("Unclear start, there are multiple possibilities")
            initial_direction = direction
        if initial_direction is None:
            raise PathError("Start is not connected to anything")
        self._direction = initial_direction

    @staticmethod
    def _char_supports_direction(char: str, direction: Direction):
        if char == HORIZONTAL:
            return direction in (Direction.LEFT, Direction.RIGHT)
        if char == VERTICAL:
            return direction in (Direction.UP, Direction.DOWN)
        return True

    def _analyze_next_move(self):
        current_char = self._map[self._map.position]
        # next if going in the same direction
        next_position = self._direction.next_position(self._map.position)
        next_char = self._map[next_position]

        if current_char in (HORIZONTAL, VERTICAL):
            if not next_char:
                raise PathError(
                    f"There is a broken path at {self._map.position}, leading to nowhere"
                )
            if not self._char_supports_direction(next_char, self._direction):
                # a sequence of -| can be both valid and invalid
                if not self._use_tunnel(self._direction):
                    raise PathError(
                        f"There is a broken path at {self._map.position}, {current_char}"
                    )
            return

        if current_char == TURN:
            surroundings = list(self._map.iter_surroundings())
            if (
                len(surroundings) == 2
                and surroundings[0][0].opposite == surroundings[1][0]
            ):
                raise PathError(
                    f'Invalid use of "{TURN}" at {self._map.position}, it should turn'
                )
        if (
            not next_char
            or not self._char_supports_direction(next_char, self._direction)
            or self._map.is_visited(next_position)
        ):
            self._handle_turn()

    def _use_tunnel(self, direction: Direction) -> bool:
        position = self._map.position
        tunnel_path = []
        while True:
            position = direction.next_position(position)
            char = self._map[position]
            if not char:
                return False
            if self._map.is_visited(position):
                tunnel_path.append(char)
                continue
            if not self._char_supports_direction(char, direction):
                return False
            self._path.extend(tunnel_path)
            # Stay in the tunnel so other logic can handle what is after the tunnel.
            # for example to collect a letter:
            #   ++
            # @--+
            #   A--x
            last_pos_in_tunnel = direction.opposite.next_position(position)
            self._map.jump_to(last_pos_in_tunnel)
            return True

    def _set_next_direction(self, revisit=False) -> bool:
        possible_tunnels = []
        for direction, position in self._map.iter_surroundings():
            if not self._char_supports_direction(self._map[position], direction):
                possible_tunnels.append(direction)
                continue
            if (
                not self._map.is_visited(position)
                or revisit
                and direction is not self._direction.opposite
            ):
                self._direction = direction
                return True
        for direction in possible_tunnels:
            if self._use_tunnel(direction):
                self._direction = direction
                return True
        return False

    def _handle_turn(self):
        if self._set_next_direction():
            return
        # priorizite going straight if all turns are already visited
        char_straight = self._map[self._direction.next_position(self._map.position)]
        if char_straight and self._char_supports_direction(
            char_straight, self._direction
        ):
            return
        if not self._set_next_direction(revisit=True):
            raise PathError(f"There is nowhere to turn at {self._map.position}")
        if self._map.position in self._possible_inifinite_loops:
            raise PathError(
                f"There is an infinite loop when following the path. Loop started at {self._map.position}"
            )
        self._possible_inifinite_loops.add(self._map.position)

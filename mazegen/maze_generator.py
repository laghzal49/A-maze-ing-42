import random
from typing import Optional, Set, Tuple, List


class Maze:
    N, E, S, W = 1, 2, 4, 8

    four_pattern = [
        (1, 1), (1, 2), (1, 3), (2, 3),
        (3, 3), (3, 4), (3, 5)
    ]

    two_pattern = [
        (0, 1), (1, 1), (2, 1),
        (2, 2),
        (0, 3), (1, 3), (2, 3),
        (0, 4),
        (0, 5), (1, 5), (2, 5)
    ]

    dirs = [
            (0, -1, N, S),
            (1, 0, E, W),
            (0, 1, S, N),
            (-1, 0, W, E),
    ]

    def __init__(self, width: int, height: int) -> None:
        """Initialize the maze with all walls intact."""
        self.width = width
        self.height = height
        self.walls: List[List[int]] = [[15 for _ in range(width)]
                                       for _ in range(height)]
        self.blocked_cells: Set[Tuple[int, int]] = set()
        self.pattern_origin: Optional[Tuple[int, int]] = None

    def in_bounds(self, x: int, y: int) -> bool:
        """Check if (x, y) is within the maze boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_blocked(self, x: int, y: int) -> bool:
        """Check if (x, y) is a blocked cell."""
        return (x, y) in self.blocked_cells

    def reset(self) -> None:
        """Reset the maze to its initial state with all walls intact."""
        for y in range(self.height):
            for x in range(self.width):
                self.walls[y][x] = 15
        self.blocked_cells.clear()
        self.pattern_origin = None

    def create_42_pattern(self) -> bool:
        """Create the 42 pattern in the maze."""
        self.blocked_cells.clear()
        self.pattern_origin = None

        max_four_x = max(dx for dx, _ in self.four_pattern)
        max_four_y = max(dy for _, dy in self.four_pattern)
        max_two_x = max(dx for dx, _ in self.two_pattern) + 5
        max_two_y = max(dy for _, dy in self.two_pattern)

        pattern_width = max(max_four_x, max_two_x) + 1
        pattern_height = max(max_four_y, max_two_y) + 1

        ox = self.width // 2 - pattern_width // 2
        oy = self.height // 2 - pattern_height // 2

        if ox < 0 or oy < 0 or ox + pattern_width > self.width or oy + \
                pattern_height > self.height:
            return False

        self.pattern_origin = (ox, oy)

        for dx, dy in self.four_pattern:
            self.blocked_cells.add((ox + dx, oy + dy))

        for dx, dy in self.two_pattern:
            self.blocked_cells.add((ox + 5 + dx, oy + dy))

        for x, y in self.blocked_cells:
            if self.in_bounds(x, y):
                self.walls[y][x] = 15
        return True

    def _carve_passage(
        self,
        cx: int,
        cy: int,
        nx: int,
        ny: int,
        w_bit: int,
        opp_bit: int,
    ) -> None:
        """Carve a passage between two cells by removing the walls."""
        self.walls[cy][cx] &= ~w_bit
        self.walls[ny][nx] &= ~opp_bit

    def _neighbors(
        self,
        x: int,
        y: int,
        visited: Optional[Set[Tuple[int, int]]] = None,
        require_unvisited: Optional[bool] = None,
        rng: Optional[random.Random] = None,
    ) -> List[Tuple[int, int, int, int]]:
        """
        Return valid neighbor cells with optional visited-state filtering."""
        directions = list(self.dirs)
        if rng is not None:
            rng.shuffle(directions)

        neighbors: List[Tuple[int, int, int, int]] = []
        for dx, dy, w_bit, opp_bit in directions:
            nx, ny = x + dx, y + dy
            if not self.in_bounds(nx, ny) or self.is_blocked(nx, ny):
                continue

            if visited is not None and require_unvisited is not None:
                is_unvisited = (nx, ny) not in visited
                if is_unvisited != require_unvisited:
                    continue

            neighbors.append((nx, ny, w_bit, opp_bit))
        return neighbors

    def _first_open_cell(self) -> list[Tuple[int, int]]:
        """Return the first non-blocked cell in row-major order."""
        for y in range(self.height):
            for x in range(self.width):
                if not self.is_blocked(x, y):
                    yield (x, y)

    def generate_maze(
        self,
        seed: Optional[int] = None,
        algo: str = "prim",
        perfect: bool = True,
    ) -> None:
        """Generate a maze using the specified algorithm."""
        rng = random.Random(seed)
        self.reset()
        self.create_42_pattern()

        algo_map = {
            "prim": self._prim_algo,
            "dfs": self._dfs_algo,
            "hunt": self._hunt_and_kill,
        }

        algo_func = algo_map.get(algo, self._prim_algo)
        algo_func(rng)

        if not perfect:
            self._add_loops(rng, loop_chance=0.1)

    def _dfs_algo(self, rng: random.Random) -> None:
        """Generate a maze using the Depth-First Search algorithm."""
        visited = set(self.blocked_cells)
        start = next(self._first_open_cell(), None)
        if not start:
            return
        stack = [start]
        visited.add(start)
        while stack:
            cx, cy = stack[-1]
            neighbors = self._neighbors(
                cx, cy, visited=visited, require_unvisited=True)
            if not neighbors:
                stack.pop()
                continue
            nx, ny, w_bit, opp_bit = rng.choice(neighbors)
            self._carve_passage(cx, cy, nx, ny, w_bit, opp_bit)
            visited.add((nx, ny))
            stack.append((nx, ny))

    def _prim_algo(self, rng: random.Random) -> None:
        """Generate a maze using Prim's algorithm."""
        visited: Set[Tuple[int, int]] = set(self.blocked_cells)

        start = next(self._first_open_cell(), None)
        if not start:
            return

        visited.add(start)
        frontier: List[Tuple[int, int, int, int, int, int]] = []

        def add_frontier(cx: int, cy: int) -> None:
            """Add the neighboring cells of (cx, cy) to the frontier."""
            for nx, ny, w_bit, opp_bit in self._neighbors(
                    cx, cy, visited=visited, require_unvisited=True):
                frontier.append((cx, cy, nx, ny, w_bit, opp_bit))

        add_frontier(start[0], start[1])

        while frontier:
            cx, cy, nx, ny, w_bit, opp_bit = frontier.pop(
                rng.randrange(len(frontier)))
            if (nx, ny) in visited:
                continue
            self._carve_passage(
                cx, cy, nx, ny, w_bit, opp_bit)
            visited.add((nx, ny))
            add_frontier(nx, ny)

    def _hunt_and_kill(self, rng: random.Random) -> None:
        """Generate a maze using the Hunt-and-Kill algorithm."""
        visited = set(self.blocked_cells)
        start = next(self._first_open_cell(), None)
        if not start:
            return

        cx, cy = start
        visited.add((cx, cy))
        while True:
            while nbrs := self._neighbors(
                    cx, cy, visited=visited, require_unvisited=True, rng=rng):
                nx, ny, w, opp = nbrs[0]
                self._carve_passage(cx, cy, nx, ny, w, opp)
                cx, cy = nx, ny
                visited.add((cx, cy))

            found = False
            for y in range(self.height):
                for x in range(self.width):
                    if (x, y) not in visited and not self.is_blocked(x, y):
                        if vn := self._neighbors(
                                x, y, visited=visited,
                                require_unvisited=False, rng=rng):
                            nx, ny, w, opp = rng.choice(vn)
                            self._carve_passage(x, y, nx, ny, w, opp)
                            cx, cy = nx, ny
                            visited.add((cx, cy))
                            found = True
                            break
                if found:
                    break
            if not found:
                return

    def _add_loops(
            self,
            rng: random.Random, loop_chance: float = 0.1) -> None:
        """Randomly add loops to the maze."""
        for y in range(self.height):
            for x in range(self.width):
                if self.is_blocked(x, y):
                    continue
                if rng.random() >= loop_chance:
                    continue
                choices = list(self._neighbors(x, y))
                if not choices:
                    continue
                nx, ny, w_bit, opp_bit = rng.choice(choices)
                self._carve_passage(
                    x, y, nx, ny, w_bit, opp_bit,
                )

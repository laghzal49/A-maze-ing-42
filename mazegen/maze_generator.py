import random
from typing import Optional, Set, Tuple, List


class Maze:
    N, E, S, W = 1, 2, 4, 8

    four_pattern = [
        (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3),
        (3, 3), (3, 4), (3, 5), (3, 6)
    ]

    two_pattern = [
        (0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (0, 3),
        (1, 3), (2, 3), (3, 3), (0, 4), (0, 5), (0, 6), (1, 6),
        (2, 6), (3, 6)
    ]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.walls: List[List[int]] = [[15 for _ in range(width)] for _ in range(height)]
        self.blocked_cells: Set[Tuple[int, int]] = set()
        self.pattern_origin: Optional[Tuple[int, int]] = None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_blocked(self, x: int, y: int) -> bool:
        return (x, y) in self.blocked_cells

    def reset(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.walls[y][x] = 15
        self.blocked_cells.clear()
        self.pattern_origin = None

    def create_42_pattern(self) -> bool:
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

        if ox < 0 or oy < 0 or ox + pattern_width > self.width or oy + pattern_height > self.height:
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

    def generate_maze(self, seed: Optional[int] = None, algo: str = "dfs",
                      perfect: bool = True) -> None:
        rng = random.Random(seed)
        self.reset()
        self.create_42_pattern()

        if algo == "prim" and not perfect:
            self._prim_algo(rng)
            self.add_loops(rng, loop_chance=0.1)
        elif algo == "prim" and perfect:
            self._prim_algo(rng)
        elif algo == "dfs" and not perfect:
            self._dfs_algo(rng)
        elif algo == "dfs" and perfect:
            self._dfs_algo(rng)

    def _dfs_algo(self, rng: random.Random) -> None:
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        for x, y in self.blocked_cells:
            if self.in_bounds(x, y):
                visited[y][x] = True

        dirs = [
            (0, -1, self.N, self.S),
            (1, 0, self.E, self.W),
            (0, 1, self.S, self.N),
            (-1, 0, self.W, self.E),
        ]

        def dfs(cx: int, cy: int) -> None:
            visited[cy][cx] = True
            d = dirs[:]
            rng.shuffle(d)
            for dx, dy, w_bit, opp_bit in d:
                nx, ny = cx + dx, cy + dy
                if not self.in_bounds(nx, ny):
                    continue
                if visited[ny][nx]:
                    continue
                if self.is_blocked(nx, ny):
                    continue
                self.walls[cy][cx] &= ~w_bit
                self.walls[ny][nx] &= ~opp_bit
                dfs(nx, ny)

        # pick first non-blocked cell
        for y in range(self.height):
            for x in range(self.width):
                if not self.is_blocked(x, y):
                    dfs(x, y)
                    return

    def _prim_algo(self, rng: random.Random) -> None:
        visited: Set[Tuple[int, int]] = set(self.blocked_cells)

        start = None
        for y in range(self.height):
            for x in range(self.width):
                if not self.is_blocked(x, y):
                    start = (x, y)
                    break
            if start:
                break
        if not start:
            return

        visited.add(start)
        frontier: List[Tuple[int, int, int, int, int, int]] = []

        def add_frontier(cx: int, cy: int) -> None:
            for dx, dy, w_bit, opp_bit in [
                (0, -1, self.N, self.S),
                (1, 0, self.E, self.W),
                (0, 1, self.S, self.N),
                (-1, 0, self.W, self.E),
            ]:
                nx, ny = cx + dx, cy + dy
                if not self.in_bounds(nx, ny):
                    continue
                if self.is_blocked(nx, ny):
                    continue
                if (nx, ny) in visited:
                    continue
                frontier.append((cx, cy, nx, ny, w_bit, opp_bit))

        add_frontier(start[0], start[1])

        while frontier:
            cx, cy, nx, ny, w_bit, opp_bit = frontier.pop(rng.randrange(len(frontier)))
            if (nx, ny) in visited:
                continue
            self.walls[cy][cx] &= ~w_bit
            self.walls[ny][nx] &= ~opp_bit
            visited.add((nx, ny))
            add_frontier(nx, ny)
        
    def add_loops(self, rng: random.Random, loop_chance: float = 0.1) -> None:
            """Randomly add loops to the maze."""
            for y in range(self.height):
                for x in range(self.width):
                    if self.is_blocked(x, y):
                        continue

                    if rng.random() >= loop_chance:
                        continue

                    choices = []
                    # North
                    if self.in_bounds(x, y - 1) and not self.is_blocked(x, y - 1):
                        choices.append((0, -1, self.N, self.S))
                    # East
                    if self.in_bounds(x + 1, y) and not self.is_blocked(x + 1, y):
                        choices.append((1, 0, self.E, self.W))
                    # South
                    if self.in_bounds(x, y + 1) and not self.is_blocked(x, y + 1):
                        choices.append((0, 1, self.S, self.N))
                    # West
                    if self.in_bounds(x - 1, y) and not self.is_blocked(x - 1, y):
                        choices.append((-1, 0, self.W, self.E))

                    if not choices:
                        continue

                    dx, dy, w_bit, opp_bit = rng.choice(choices)
                    self.walls[y][x] &= ~w_bit
                    self.walls[y + dy][x + dx] &= ~opp_bit

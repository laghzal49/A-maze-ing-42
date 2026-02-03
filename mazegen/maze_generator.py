"""Maze generation core."""

import random
from typing import Optional, Set, Tuple, List


class Maze:
    """Maze grid with wall bitmasks and 42 pattern support."""

    # Direction bitmasks
    N, E, S, W = 1, 2, 4, 8

    # "4" Digit relative coordinates
    four_pattern = [
        (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3),
        (3, 3), (3, 4), (3, 5), (3, 6)
    ]

    # "2" Digit relative coordinates
    two_pattern = [
        (0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (0, 3),
        (1, 3), (2, 3), (3, 3), (0, 4), (0, 5), (0, 6), (1, 6),
        (2, 6), (3, 6)
    ]

    def __init__(self: "Maze", width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.walls: List[List[int]] = [
            [15 for _ in range(width)] for _ in range(height)
        ]
        self.blocked_cells: Set[Tuple[int, int]] = set()
        self.pattern_origin: Optional[Tuple[int, int]] = None

    def in_bounds(self: "Maze", x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_blocked(self: "Maze", x: int, y: int) -> bool:
        return (x, y) in self.blocked_cells

    def create_42_pattern(self: "Maze") -> bool:
        """Mark the '42' cells as blocked. Returns True if placed."""
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

        if (
            ox < 0
            or oy < 0
            or ox + pattern_width > self.width
            or oy + pattern_height > self.height
        ):
            return False

        self.pattern_origin = (ox, oy)

        # Add "4"
        for dx, dy in self.four_pattern:
            nx, ny = ox + dx, oy + dy
            if self.in_bounds(nx, ny):
                self.blocked_cells.add((nx, ny))

        # Add "2" (shifted right)
        for dx, dy in self.two_pattern:
            nx, ny = ox + 5 + dx, oy + dy
            if self.in_bounds(nx, ny):
                self.blocked_cells.add((nx, ny))

        # Force blocked cells to be fully closed
        for x, y in self.blocked_cells:
            self.walls[y][x] = 15
        return True

    def reset(self: "Maze") -> None:
        """Reset the grid (all closed)."""
        for y in range(self.height):
            for x in range(self.width):
                self.walls[y][x] = 15
        self.blocked_cells.clear()
        self.pattern_origin = None

    def generate_maze(
        self: "Maze",
        seed: Optional[int] = None,
        algo: str = "dfs",
        perfect: bool = True,
    ) -> None:
        """Main entry: reset, lock the 42 pattern, then generate."""
        rng = random.Random(seed)

        self.reset()
        self.create_42_pattern()

        if perfect and algo == "binary_tree":
            self._dfs_algo(rng)
        elif algo == "binary_tree":
            self._binary_tree_algo(rng)
        elif algo == "prim":
            self._prim_algo(rng)
        else:
            self._dfs_algo(rng)
        self._ensure_connected(rng)

    def generate(
        self: "Maze",
        seed: Optional[int] = None,
        algo: str = "dfs",
        perfect: bool = True,
    ) -> None:
        """Compatibility wrapper for generate_maze."""
        self.generate_maze(seed=seed, algo=algo, perfect=perfect)

    def _dfs_algo(self: "Maze", rng: random.Random) -> None:
        """DFS recursive backtracker spanning all reachable cells."""
        visited = [[False for _ in range(self.width)]
                   for _ in range(self.height)]

        for x, y in self.blocked_cells:
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

        dfs(start[0], start[1])

    def _binary_tree_algo(self: "Maze", rng: random.Random) -> None:
        """Binary tree carving that never touches blocked cells."""
        for y in range(self.height):
            for x in range(self.width):
                if self.is_blocked(x, y):
                    continue

                choices = []
                # East
                if self.in_bounds(x + 1, y) and not self.is_blocked(x + 1, y):
                    choices.append((1, 0, self.E, self.W))
                # South
                if self.in_bounds(x, y + 1) and not self.is_blocked(x, y + 1):
                    choices.append((0, 1, self.S, self.N))

                if not choices:
                    continue

                dx, dy, w_bit, opp_bit = rng.choice(choices)
                self.walls[y][x] &= ~w_bit
                self.walls[y + dy][x + dx] &= ~opp_bit

    def _prim_algo(self: "Maze", rng: random.Random) -> None:
        """Randomized Prim's algorithm for perfect mazes."""
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
            idx = rng.randrange(len(frontier))
            cx, cy, nx, ny, w_bit, opp_bit = frontier.pop(idx)
            if (nx, ny) in visited:
                continue
            self.walls[cy][cx] &= ~w_bit
            self.walls[ny][nx] &= ~opp_bit
            visited.add((nx, ny))
            add_frontier(nx, ny)

    def _ensure_connected(self: "Maze", rng: random.Random) -> None:
        """Connect all non-blocked cells into a single component."""
        total_cells = []
        for y in range(self.height):
            for x in range(self.width):
                if not self.is_blocked(x, y):
                    total_cells.append((x, y))

        if not total_cells:
            return

        def idx(x: int, y: int) -> int:
            return y * self.width + x

        parent = list(range(self.width * self.height))
        rank = [0] * (self.width * self.height)

        def find(a: int) -> int:
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                parent[ra] = rb
            elif rank[ra] > rank[rb]:
                parent[rb] = ra
            else:
                parent[rb] = ra
                rank[ra] += 1

        edges = []
        for y in range(self.height):
            for x in range(self.width):
                if self.is_blocked(x, y):
                    continue
                if self.in_bounds(x + 1, y) and not self.is_blocked(x + 1, y):
                    edges.append((x, y, x + 1, y, self.E, self.W))
                    if not (self.walls[y][x] & self.E):
                        union(idx(x, y), idx(x + 1, y))
                if self.in_bounds(x, y + 1) and not self.is_blocked(x, y + 1):
                    edges.append((x, y, x, y + 1, self.S, self.N))
                    if not (self.walls[y][x] & self.S):
                        union(idx(x, y), idx(x, y + 1))

        rng.shuffle(edges)
        for x, y, nx, ny, w_bit, opp_bit in edges:
            if find(idx(x, y)) == find(idx(nx, ny)):
                continue
            self.walls[y][x] &= ~w_bit
            self.walls[ny][nx] &= ~opp_bit
            union(idx(x, y), idx(nx, ny))

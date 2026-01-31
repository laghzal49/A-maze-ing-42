import random
from typing import Optional, Set, Tuple


class Maze:
    """Represents a maze using wall bit-flags for each cell.
    Each cell stores a byte encoding which walls are present:
    - N (1): North wall
    - E (2): East wall
    - S (4): South wall
    - W (8): West wall
    Attributes:
        width (int): Width of maze in cells
        height (int): Height of maze in cells
        walls (list): 2D array of wall configurations (bit-flags)
    """
    N = 1  # North wall flag
    E = 2  # East wall flag
    S = 4  # South wall flag
    W = 8  # West wall flag

    def __init__(self, width: int, height: int):
        """Initialize maze with given dimensions, all walls closed.

        Args:
            width (int): Width of the maze
            height (int): Height of the maze
        """
        self.width = width
        self.height = height
        self._all_closed = self.N | self.E | self.S | self.W
        self.walls = [[self._all_closed for _ in range(self.width)]
                      for _ in range(self.height)]

    def reset(self) -> None:
        """Reset maze to all walls closed."""
        self.walls = [[self._all_closed for _ in range(self.width)]
                      for _ in range(self.height)]

    def in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates are within maze bounds.
        Args:
            x (int): X coordinate
            y (int): Y coordinate
        Returns:
            bool: True if coordinates are valid
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def carve_between(self, x: int, y: int, nx: int, ny: int) -> bool:
        """Carve a passage between two adjacent cells.
        Args:
            x (int): Current cell X
            y (int): Current cell Y
            nx (int): Next cell X
            ny (int): Next cell Y
        Returns:
            bool: True if passage was carved, False if invalid
        """
        if not (self.in_bounds(x, y) and self.in_bounds(nx, ny)):
            return False

        dx, dy = nx - x, ny - y
        mapping = {
            (0, -1): (self.N, self.S),
            (1, 0):  (self.E, self.W),
            (0, 1):  (self.S, self.N),
            (-1, 0): (self.W, self.E),
        }
        if (dx, dy) not in mapping:
            return False

        w1, w2 = mapping[(dx, dy)]
        self.walls[y][x] &= ~w1
        self.walls[ny][nx] &= ~w2
        return True

    def generate(self, entry_x: int, entry_y: int,
                 exit_x: Optional[int] = None, exit_y: Optional[int] = None,
                 seed: Optional[int] = None, algo: str = "dfs") -> None:
        """Generate maze using specified algorithm.
        Args:
            entry_x (int): Entry X coordinate
            entry_y (int): Entry Y coordinate
            exit_x (Optional[int]): Exit X coordinate (default: width-1)
            exit_y (Optional[int]): Exit Y coordinate (default: height-1)
            seed (Optional[int]): Random seed for reproducibility
            algo (str): Algorithm to use ('dfs' or 'binary_tree')
        Raises:
            ValueError: If entry/exit is out of bounds or algo is unknown
        """
        if not self.in_bounds(entry_x, entry_y):
            raise ValueError("Entry is out of bounds")

        # Set default exit if not provided
        if exit_x is None:
            exit_x = self.width - 1
        if exit_y is None:
            exit_y = self.height - 1

        if not self.in_bounds(exit_x, exit_y):
            raise ValueError("Exit is out of bounds")

        self.reset()
        rng = random.Random(seed)

        if algo == "dfs":
            visited: Set[Tuple[int, int]] = set()
            self._gen_dfs(entry_x, entry_y, visited, rng)
        elif algo == "binary_tree":
            self.generate_binary_tree(rng)
        else:
            raise ValueError(f"Unknown algo: {algo}")

        # Carve out entry point (open outer wall)
        if entry_x == 0:
            self.walls[entry_y][entry_x] &= ~self.W  # Open West wall
        elif entry_x == self.width - 1:
            self.walls[entry_y][entry_x] &= ~self.E  # Open East wall

        if entry_y == 0:
            self.walls[entry_y][entry_x] &= ~self.N  # Open North wall
        elif entry_y == self.height - 1:
            self.walls[entry_y][entry_x] &= ~self.S  # Open South wall

        # Carve out exit point (open outer wall)
        if exit_x == 0:
            self.walls[exit_y][exit_x] &= ~self.W  # Open West wall
        elif exit_x == self.width - 1:
            self.walls[exit_y][exit_x] &= ~self.E  # Open East wall

        if exit_y == 0:
            self.walls[exit_y][exit_x] &= ~self.N  # Open North wall
        elif exit_y == self.height - 1:
            self.walls[exit_y][exit_x] &= ~self.S  # Open South wall

    def _gen_dfs(
        self,
        x: int,
        y: int,
        visited: Set[Tuple[int, int]],
        rng: random.Random
    ) -> None:
        """Generate maze using Depth-First Search algorithm.
        Args:
            x (int): Current X coordinate
            y (int): Current Y coordinate
            visited (Set): Set of visited cells
            rng (random.Random): Random number generator
        """
        visited.add((x, y))
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        rng.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny) and (nx, ny) not in visited:
                self.carve_between(x, y, nx, ny)
                self._gen_dfs(nx, ny, visited, rng)

    def generate_binary_tree(self, rng: random.Random) -> None:
        """Generate maze using Binary Tree algorithm.
        Args:
            rng (random.Random): Random number generator
        """
        for y in range(self.height):
            for x in range(self.width):
                neighbors = []
                if self.in_bounds(x, y - 1):
                    neighbors.append((x, y - 1))
                if self.in_bounds(x + 1, y):
                    neighbors.append((x + 1, y))
                if neighbors:
                    nx, ny = rng.choice(neighbors)
                    self.carve_between(x, y, nx, ny)

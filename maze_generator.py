import random
from typing import Optional


class Maze:
    WALL = 1
    PATH = 0

    def __init__(self, width: int, height: int):
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        self.grid = [
            [self.WALL for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def generation(self, start_x: int, start_y: int,
                   perfect: bool = True, seed: Optional[int] = None) -> None:
        rng = random.Random(seed) if seed is not None else random

        stack = [(start_x, start_y)]
        self.grid[start_y][start_x] = self.PATH

        while stack:
            x, y = stack[-1]
            moves = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            rng.shuffle(moves)

            found = False
            for dx, dy in moves:
                nx, ny = x + dx, y + dy

                if (0 <= nx < self.width and 0 <= ny < self.height and
                        self.grid[ny][nx] == self.WALL):
                    self.grid[y + dy // 2][x + dx // 2] = self.PATH
                    self.grid[ny][nx] = self.PATH
                    stack.append((nx, ny))
                    found = True
                    break

            if not found:
                stack.pop()

        if not perfect:
            self._make_imperfect(rng)

    def _make_imperfect(self, rng):
        count = (self.width * self.height) // 20
        for _ in range(count):
            rx = rng.randrange(1, self.width - 1)
            ry = rng.randrange(1, self.height - 1)
            self.grid[ry][rx] = self.PATH

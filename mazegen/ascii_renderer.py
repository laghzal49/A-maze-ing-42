"""ASCII fallback renderer with symbol priority."""

from typing import List, Optional, Tuple

from .maze_generator import Maze


def _is_wall_between(maze: Maze, x: int, y: int, dx: int, dy: int) -> bool:
    nx, ny = x + dx, y + dy
    if not maze.in_bounds(nx, ny):
        return True
    if maze.is_blocked(x, y) or maze.is_blocked(nx, ny):
        return True
    cell = maze.walls[y][x]
    if dx == 0 and dy == -1:
        return bool(cell & maze.N)
    if dx == 1 and dy == 0:
        return bool(cell & maze.E)
    if dx == 0 and dy == 1:
        return bool(cell & maze.S)
    if dx == -1 and dy == 0:
        return bool(cell & maze.W)
    return True


class AsciiCorner:
    @staticmethod
    def get_corner(left: bool, right: bool, up: bool, down: bool) -> str:
        if up and down and left and right:
            return "╋"
        elif up and down and left and not right:
            return "┫"
        elif up and down and not left and right:
            return "┣"
        elif up and not down and left and right:
            return "┻"
        elif not up and down and left and right:
            return "┳"
        elif up and down and not left and not right:
            return "┃"
        elif not up and not down and left and right:
            return "━"
        elif up and not down and left and not right:
            return "┛"
        elif up and not down and not left and right:
            return "┗"
        elif not up and down and left and not right:
            return "┓"
        elif not up and down and not left and right:
            return "┏"
        elif up and not down and not left and not right:
            return "┃"
        elif not up and down and not left and not right:
            return "┃"
        elif not up and not down and left and not right:
            return "━"
        elif not up and not down and not left and right:
            return "━"
        return " "


def render_maze(
    maze: Maze,
    path: Optional[List[Tuple[int, int]]] = None,
    start: Optional[Tuple[int, int]] = None,
    end: Optional[Tuple[int, int]] = None,
) -> None:
    """Render a static ASCII version of the maze."""
    w, h = maze.width, maze.height

    horiz = [[False for _ in range(w)] for _ in range(h + 1)]
    vert = [[False for _ in range(h)] for _ in range(w + 1)]

    for jy in range(h + 1):
        for x in range(w):
            if jy == 0:
                horiz[jy][x] = _is_wall_between(maze, x, 0, 0, -1)
            elif jy == h:
                horiz[jy][x] = _is_wall_between(maze, x, h - 1, 0, 1)
            else:
                horiz[jy][x] = _is_wall_between(maze, x, jy - 1, 0, 1)

    for jx in range(w + 1):
        for y in range(h):
            if jx == 0:
                vert[jx][y] = _is_wall_between(maze, 0, y, -1, 0)
            elif jx == w:
                vert[jx][y] = _is_wall_between(maze, w - 1, y, 1, 0)
            else:
                vert[jx][y] = _is_wall_between(maze, jx - 1, y, 1, 0)

    for jy in range(h + 1):
        wall_parts: List[str] = []
        for jx in range(w + 1):
            left = horiz[jy][jx - 1] if jx > 0 else False
            right = horiz[jy][jx] if jx < w else False
            up = vert[jx][jy - 1] if jy > 0 else False
            down = vert[jx][jy] if jy < h else False
            wall_parts.append(AsciiCorner.get_corner(left, right, up, down))
            if jx < w:
                wall_parts.append("━━━" if horiz[jy][jx] else "   ")
        print("".join(wall_parts))

        if jy == h:
            break

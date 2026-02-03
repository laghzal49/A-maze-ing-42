"""ASCII fallback renderer with symbol priority."""

from typing import List, Optional, Tuple

from .maze_generator import Maze


def render_maze(
    maze: Maze,
    path: Optional[List[Tuple[int, int]]] = None,
    start: Optional[Tuple[int, int]] = None,
    end: Optional[Tuple[int, int]] = None,
) -> None:
    """Render a static ASCII version of the maze."""
    w, h = maze.width, maze.height
    path_set = set(path) if path else set()

    print("+" + "---+" * w)

    for y in range(h):
        line1 = "|"
        line2 = "+"

        for x in range(w):
            cell = maze.walls[y][x]

            # --- LINE 1: CONTENT ---
            if start is not None and (x, y) == start:
                content = " @ "
            elif (x, y) == end:
                content = " E "
            elif (x, y) in path_set:
                content = " . "
            elif maze.is_blocked(x, y):
                content = "███"
            else:
                content = "   "
            line1 += content

            # Right Wall
            if maze.is_blocked(x, y):
                line1 += "█"
            else:
                line1 += "|" if (cell & maze.E) else " "

            # --- LINE 2: BOTTOM WALL ---
            if maze.is_blocked(x, y):
                line2 += "███+"
            else:
                line2 += "---+" if (cell & maze.S) else "   +"

        print(line1)
        print(line2)

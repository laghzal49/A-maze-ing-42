"""Breadth-First Search pathfinder and move sequence generator."""

import queue
from typing import List, Tuple, Optional

from .maze_generator import Maze


def bfs_find_path(
    maze: Maze,
    start: Tuple[int, int],
    end: Tuple[int, int],
) -> Optional[List[Tuple[int, int]]]:
    """Find the shortest path avoiding blocked cells and walls."""
    if not (maze.in_bounds(*start) and maze.in_bounds(*end)):
        return None
    if maze.is_blocked(*start) or maze.is_blocked(*end):
        return None

    visited = {start}
    q = queue.Queue()
    q.put((start, [start]))

    # Mapping relative movement to the wall bit that must be OPEN
    w_map = {
        (0, -1): 1,  # North (Maze.N)
        (1, 0): 2,   # East (Maze.E)
        (0, 1): 4,   # South (Maze.S)
        (-1, 0): 8   # West (Maze.W)
    }

    while not q.empty():
        (cx, cy), path = q.get()
        if (cx, cy) == end:
            return path

        for (dx, dy), bit in w_map.items():
            nx, ny = cx + dx, cy + dy
            if maze.in_bounds(nx, ny) and not maze.is_blocked(nx, ny):
                # Check if the wall bit is NOT set (meaning passage is open)
                if not (maze.walls[cy][cx] & bit):
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        q.put(((nx, ny), path + [(nx, ny)]))
    return None


def path_to_moves(path: List[Tuple[int, int]]) -> str:
    """Convert a list of coordinates into a N/E/S/W direction string."""
    if not path or len(path) < 2:
        return ""

    moves = []
    # (dx, dy) mapping
    dir_map = {
        (0, -1): "N",
        (1, 0): "E",
        (0, 1): "S",
        (-1, 0): "W"
    }

    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        move = dir_map.get((x2 - x1, y2 - y1))
        if move:
            moves.append(move)

    return "".join(moves)

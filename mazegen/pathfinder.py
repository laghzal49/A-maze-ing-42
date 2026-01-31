"""
This file has been replaced by path_finder.py

The new path_finder.py uses A* (A-star) algorithm:
- Faster than BFS (2-10x speedup)
- Still guarantees shortest path
- Uses Manhattan distance heuristic
- Priority queue (heap) for efficient exploration

Functions:
    - astar_find_path(): A* pathfinding (fastest)
    - bfs_find_path(): Alias to astar_find_path
    - path_to_moves(): Convert path to "NESW" string

Usage:
    from mazegen.path_finder import astar_find_path, path_to_moves
    from mazegen.maze_generator import Maze

    maze = Maze(20, 15)
    maze.generate(0, 0, exit_x=19, exit_y=14)

    path = astar_find_path(maze, (0, 0), (19, 14))
    if path:
        moves = path_to_moves(path)
        print(f"Path: {moves}")
"""

# For backwards compatibility
from .path_finder import astar_find_path, bfs_find_path, path_to_moves

__all__ = ["astar_find_path", "bfs_find_path", "path_to_moves"]

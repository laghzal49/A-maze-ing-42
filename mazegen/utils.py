"""
Utility functions for maze operations.

This module has been refactored. Functionality is now distributed:
- maze_generator.py: Core maze operations
- path_finder.py: Pathfinding utilities
- forth_two.py: Pattern utilities
- parser.py: Config utilities
"""

from .maze_generator import Maze


def print_maze_info(maze: Maze) -> None:
    """Print maze statistics."""
    total_cells = maze.width * maze.height
    print(f"Maze dimensions: {maze.width}x{maze.height}")
    print(f"Total cells: {total_cells}")


def count_open_passages(maze: Maze) -> int:
    """Count total open passages in maze."""
    count = 0
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.walls[y][x]
            # Count open walls (0 bits)
            for direction in [Maze.N, Maze.E, Maze.S, Maze.W]:
                if not (cell & direction):
                    count += 1
    # Each passage counted twice (from both sides)
    return count // 2


def is_perfect_maze(maze: Maze) -> bool:
    """Check if maze is perfect (no loops, all cells connected)."""
    # Perfect maze has exactly (width * height - 1) passages
    expected = maze.width * maze.height - 1
    actual = count_open_passages(maze)
    return actual == expected


__all__ = ["print_maze_info", "count_open_passages", "is_perfect_maze"]

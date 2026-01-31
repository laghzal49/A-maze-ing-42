"""
This file has been replaced by maze_generator.py + forth_two.py

The new implementation:
- maze_generator.py: Core Maze class with generation algorithms
- forth_two.py: "42" pattern display logic

The "42" pattern is now rendered as colored cells in the pygame GUI,
automatically positioned to avoid the solution path.

Usage:
    from mazegen.maze_generator import Maze
    from mazegen.forth_two import get_42_pattern, find_42_location

    maze = Maze(30, 20)
    maze.generate(0, 0, exit_x=29, exit_y=19, algo='dfs')

    # Get 42 pattern cells
    fortytwo_cells = get_42_pattern(5, 5)
"""

# For backwards compatibility
from .maze_generator import Maze
from .forth_two import get_42_pattern, find_42_location

__all__ = ["Maze", "get_42_pattern", "find_42_location"]

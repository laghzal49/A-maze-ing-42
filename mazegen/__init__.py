"""
Mazegen package - Maze generation and solving with pygame visualization.

Modules:
    - maze_generator: Core maze generation (DFS, Binary Tree)
    - path_finder: A* pathfinding algorithm
    - parser: Configuration file parsing
    - forth_two: "42" pattern display
    - render: Pygame interactive renderer

Usage:
    python3 -m mazegen          # CLI demo
    python3 -m mazegen.render   # Interactive GUI
"""

__version__ = "2.0.0"
__all__ = [
    "Maze",
    "astar_find_path",
    "bfs_find_path",
    "path_to_moves",
    "MazeConfig",
    "parse_file",
    "MazeRenderer",
    "is_perfect_maze",
    "validate_entry_exit",
    "has_multiple_paths",
]

from .maze_generator import Maze
from .path_finder import astar_find_path, bfs_find_path, path_to_moves
from .parser import MazeConfig, parse_file
from .render import MazeRenderer
from .maze_validator import is_perfect_maze, validate_entry_exit, has_multiple_paths

"""A-maze-ing: A maze generator with 42 pattern integration."""

from mazegen.maze_generator import Maze
from mazegen.maze_42_generator import generate_perfect_maze_with_42
from mazegen.pathfinder import solve_maze
from mazegen.maze_renderer import display_terminal
from mazegen.config_parser import parser
from mazegen.utils import (
    encode_cell_walls,
    save_maze_to_file,
    force_path,
    get_dynamic_sleep,
)

__all__ = [
    "Maze",
    "generate_perfect_maze_with_42",
    "solve_maze",
    "display_terminal",
    "parser",
    "encode_cell_walls",
    "save_maze_to_file",
    "force_path",
    "get_dynamic_sleep",
]

import curses
from typing import Optional, Tuple, Set

from .maze_generator import Maze
from .path_finder import bfs_find_path
from .curses_renderer import render_maze_curses
from .ascii_renderer import render_maze


class MazeRenderer:
    """Terminal renderer with curses support."""

    def __init__(
        self: "MazeRenderer",
        width: int,
        height: int,
        cell_size: int = 25,
        entry: Optional[Tuple[int, int]] = None,
        exit: Optional[Tuple[int, int]] = None,
        seed: Optional[int] = None,
        algo: str = "dfs",
        perfect: bool = True,
        use_curses: bool = True,
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.algo = algo
        self.perfect = perfect
        self.use_curses = use_curses

    def _build_maze(self: "MazeRenderer") -> Maze:
        """Build a maze instance."""
        maze = Maze(self.width, self.height)
        maze.generate_maze(seed=self.seed, algo=self.algo,
                           perfect=self.perfect)
        return maze

    def run(self: "MazeRenderer") -> None:
        """Run the maze renderer."""
        maze = self._build_maze()
        start = self.entry
        end = self.exit
        if (start and start in maze.blocked_cells) or (
            end and end in maze.blocked_cells
        ):
            raise ValueError("Entry or exit position is blocked.")
        path = None
        if start and end:
            try:
                path = bfs_find_path(maze, start, end)
            except ValueError:
                path = None

        if self.use_curses:
            try:
                curses.wrapper(
                    render_maze_curses,
                    maze,
                    start,
                    end,
                    self.algo,
                    self.seed,
                    self.perfect,
                    None,
                )
            except Exception as e:
                print(f"Curses error: {e}")
                print("Falling back to ASCII render...")
                render_maze(maze, path=path, start=start, end=end)
        else:
            render_maze(maze, path=path, start=start, end=end)


def _get_42_cells(maze: Maze) -> Set[Tuple[int, int]]:
    """Get all cells that are part of the 42 pattern."""
    return maze.blocked_cells

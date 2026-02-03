"""Test suite for maze generation and pathfinding."""

from mazegen.maze_generator import Maze
from mazegen.path_finder import bfs_find_path, path_to_moves
from mazegen.parser import parse_dict


def test_maze_creation() -> None:
    """Test basic maze creation."""
    maze = Maze(10, 10)
    assert maze.width == 10
    assert maze.height == 10


def test_maze_generation() -> None:
    """Test maze generation algorithms."""
    maze = Maze(15, 12)

    maze.generate_maze(seed=42, algo="dfs", perfect=True)
    assert maze.walls[0][0] is not None

    maze.generate_maze(seed=42, algo="binary_tree", perfect=False)
    assert maze.walls[0][0] is not None


def test_pathfinding() -> None:
    """Test BFS pathfinding."""
    maze = Maze(10, 10)
    maze.generate_maze(seed=42, algo="dfs", perfect=True)

    path = bfs_find_path(maze, (0, 0), (9, 9))
    assert path is not None
    assert len(path) > 0
    assert path[0] == (0, 0)
    assert path[-1] == (9, 9)


def test_path_to_moves() -> None:
    """Test path to moves conversion."""
    path = [(0, 0), (1, 0), (1, 1), (1, 2)]
    moves = path_to_moves(path)
    assert moves == "ESS"


def test_config_validation() -> None:
    """Test configuration validation."""
    config = parse_dict({
        "width": 20,
        "height": 15,
        "entry": (0, 0),
        "exit": (19, 14),
        "perfect": True,
        "output_file": "maze.txt",
    })
    assert config.width == 20

    try:
        parse_dict({
            "width": 10,
            "height": 10,
            "entry": (15, 15),
            "exit": (9, 9),
            "perfect": True,
            "output_file": "maze.txt",
        })
        assert False, "Invalid config accepted"
    except ValueError:
        pass


def test_42_pattern() -> None:
    """Test 42 pattern placement."""
    maze = Maze(30, 20)
    placed = maze.create_42_pattern()
    assert placed
    assert len(maze.blocked_cells) > 0

    small_maze = Maze(5, 5)
    placed_small = small_maze.create_42_pattern()
    assert not placed_small

"""
Test suite for maze generation and pathfinding.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mazegen.maze_generator import Maze
from mazegen.path_finder import astar_find_path, path_to_moves
from mazegen.parser import MazeConfig, parse_dict
from mazegen.forth_two import get_42_pattern, find_42_location


def test_maze_creation():
    """Test basic maze creation."""
    maze = Maze(10, 10)
    assert maze.width == 10
    assert maze.height == 10
    print("✓ Maze creation test passed")


def test_maze_generation():
    """Test maze generation algorithms."""
    maze = Maze(15, 12)
    
    # Test DFS
    maze.generate(0, 0, exit_x=14, exit_y=11, seed=42, algo='dfs')
    assert maze.walls[0][0] is not None
    print("✓ DFS generation test passed")
    
    # Test Binary Tree
    maze.generate(0, 0, exit_x=14, exit_y=11, seed=42, algo='binary_tree')
    assert maze.walls[0][0] is not None
    print("✓ Binary Tree generation test passed")


def test_pathfinding():
    """Test A* pathfinding."""
    maze = Maze(10, 10)
    maze.generate(0, 0, exit_x=9, exit_y=9, seed=42, algo='dfs')
    
    path = astar_find_path(maze, (0, 0), (9, 9))
    assert path is not None
    assert len(path) > 0
    assert path[0] == (0, 0)
    assert path[-1] == (9, 9)
    print(f"✓ Pathfinding test passed (path length: {len(path)})")


def test_path_to_moves():
    """Test path to moves conversion."""
    path = [(0, 0), (1, 0), (1, 1), (1, 2)]
    moves = path_to_moves(path)
    assert moves == "ESS"
    print("✓ Path to moves test passed")


def test_config_validation():
    """Test configuration validation."""
    # Valid config
    try:
        config = parse_dict({
            'width': 20,
            'height': 15,
            'entry': (0, 0),
            'exit': (19, 14),
            'perfect': True,
            'output_file': 'maze.txt'
        })
        assert config.width == 20
        print("✓ Valid config test passed")
    except ValueError:
        assert False, "Valid config rejected"
    
    # Invalid config (entry out of bounds)
    try:
        parse_dict({
            'width': 10,
            'height': 10,
            'entry': (15, 15),
            'exit': (9, 9),
            'perfect': True,
            'output_file': 'maze.txt'
        })
        assert False, "Invalid config accepted"
    except ValueError:
        print("✓ Invalid config rejection test passed")


def test_42_pattern():
    """Test 42 pattern generation."""
    cells = get_42_pattern(0, 0)
    assert len(cells) > 0
    assert (0, 0) in cells  # Top-left of '4'
    print(f"✓ 42 pattern test passed ({len(cells)} cells)")


def test_42_location_finder():
    """Test 42 location finding with path avoidance."""
    maze = Maze(30, 20)
    maze.generate(0, 0, exit_x=29, exit_y=19, seed=42, algo='dfs')
    
    path = astar_find_path(maze, (0, 0), (29, 19))
    path_set = set(path) if path else set()
    
    location = find_42_location(maze, path_set)
    pattern_cells = get_42_pattern(location[0], location[1])
    
    # Verify no overlap with path
    overlap = pattern_cells & path_set
    assert len(overlap) == 0, f"42 pattern overlaps with path: {overlap}"
    print("✓ 42 location finder test passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running Maze Tests")
    print("=" * 60)
    
    test_maze_creation()
    test_maze_generation()
    test_pathfinding()
    test_path_to_moves()
    test_config_validation()
    test_42_pattern()
    test_42_location_finder()
    
    print("=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()

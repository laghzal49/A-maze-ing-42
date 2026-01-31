"""
Module to create '42' pattern in maze.
"""

from .maze_generator import Maze
from typing import Set, Tuple


def get_42_pattern(start_x: int, start_y: int) -> Set[Tuple[int, int]]:
    """
    Get the cell coordinates that form the '42' pattern.
    Each digit is 3 cells wide and 5 cells tall.

    Args:
        start_x: Starting x coordinate
        start_y: Starting y coordinate

    Returns:
        Set of (x, y) coordinates forming '42'
    """
    # Pattern for '4' (3x5)
    four_pattern = [
        (0, 0), (0, 1), (0, 2),  # Left vertical
        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),  # Right vertical
        (1, 2),  # Middle horizontal connection
    ]

    # Pattern for '2' (3x5)
    two_pattern = [
        (0, 0), (1, 0), (2, 0),  # Top horizontal
        (2, 1),  # Right side
        (0, 2), (1, 2), (2, 2),  # Middle horizontal
        (0, 3),  # Left side
        (0, 4), (1, 4), (2, 4),  # Bottom horizontal
    ]

    cells = set()

    # Add '4' cells
    for dx, dy in four_pattern:
        cells.add((start_x + dx, start_y + dy))

    # Add '2' cells (4 cells to the right with 1 cell gap)
    two_start_x = start_x + 4
    for dx, dy in two_pattern:
        cells.add((two_start_x + dx, start_y + dy))

    return cells


def find_42_location(maze: Maze, avoid_path: set = None) -> Tuple[int, int]:
    """
    Find a good location for '42' pattern that doesn't conflict with path.

    Args:
        maze: Maze object
        avoid_path: Set of (x, y) coordinates to avoid (path cells)

    Returns:
        (start_x, start_y) tuple for the pattern
    """
    if avoid_path is None:
        avoid_path = set()

    # Try to find a good location for '42' (needs 7x5 space)
    # Check all possible positions
    for start_y in range(maze.height - 5):
        for start_x in range(maze.width - 7):
            # Get the actual 42 pattern cells for this position
            pattern_cells = get_42_pattern(start_x, start_y)
            
            # Check if ANY pattern cell conflicts with path
            conflict = False
            for cell in pattern_cells:
                if cell in avoid_path or not maze.in_bounds(cell[0], cell[1]):
                    conflict = True
                    break
            
            if not conflict:
                return (start_x, start_y)

    # If no good spot found, try edge locations
    edge_locations = [
        (1, 1),
        (maze.width - 8, 1),
        (1, maze.height - 6),
        (maze.width - 8, maze.height - 6)
    ]
    
    for start_x, start_y in edge_locations:
        if start_x >= 0 and start_y >= 0:
            pattern_cells = get_42_pattern(start_x, start_y)
            conflict = any(cell in avoid_path for cell in pattern_cells)
            if not conflict:
                return (start_x, start_y)
    
    # Last resort - top corner
    return (1, 1)

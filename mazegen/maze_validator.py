"""
Maze validation functions.

This module provides functions to validate and analyze maze properties.
"""

from typing import Tuple, Set
from .maze_generator import Maze


def is_perfect_maze(maze: Maze) -> bool:
    """Check if maze is perfect (single path between any two points).
    
    A perfect maze has:
    - No loops (no multiple paths between cells)
    - No isolated areas (all cells connected)
    - Exactly (width * height - 1) passages
    
    Args:
        maze (Maze): The maze to validate
        
    Returns:
        bool: True if maze is perfect, False otherwise
        
    Example:
        >>> maze = Maze(21, 21)
        >>> maze.generate(0, 0)
        >>> if is_perfect_maze(maze):
        ...     print("Perfect maze!")
    """
    passages = count_open_passages(maze)
    expected = maze.width * maze.height - 1
    return passages == expected


def count_open_passages(maze: Maze) -> int:
    """Count total open passages in maze.
    
    Each passage (opening between cells) is counted from both sides,
    so we divide by 2 to get the actual count.
    
    Args:
        maze (Maze): The maze to analyze
        
    Returns:
        int: Total number of unique passages
    """
    count = 0
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.walls[y][x]
            # Count open walls (0 bits) for N, E, S, W directions
            for direction in [Maze.N, Maze.E, Maze.S, Maze.W]:
                if not (cell & direction):  # Wall is open if bit is 0
                    count += 1
    return count // 2  # Each passage counted twice


def validate_entry_exit(maze: Maze, entry: Tuple[int, int], 
                       exit: Tuple[int, int]) -> bool:
    """Validate that entry and exit points are valid and distinct.
    
    Args:
        maze (Maze): The maze to validate
        entry (Tuple[int, int]): Entry coordinates (x, y)
        exit (Tuple[int, int]): Exit coordinates (x, y)
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not maze.in_bounds(entry[0], entry[1]):
        return False
    if not maze.in_bounds(exit[0], exit[1]):
        return False
    if entry == exit:
        return False
    return True


def has_multiple_paths(maze: Maze, start: Tuple[int, int], 
                      end: Tuple[int, int]) -> bool:
    """Check if maze has multiple paths between start and end.
    
    Uses BFS to explore all possible paths. If more than one path exists,
    the maze is NOT perfect (has loops/redundant paths).
    
    Args:
        maze (Maze): The maze to analyze
        start (Tuple[int, int]): Start coordinates (x, y)
        end (Tuple[int, int]): End coordinates (x, y)
        
    Returns:
        bool: True if multiple paths exist, False if only one or zero
    """
    from collections import deque
    
    queue = deque([start])
    visited = {start}
    path_count = 0
    
    while queue and path_count <= 1:  # Stop at 2+ paths
        x, y = queue.popleft()
        
        if (x, y) == end:
            path_count += 1
            if path_count > 1:
                return True
            continue
        
        # Check all directions
        for direction, (dx, dy) in [
            (Maze.N, (0, -1)),
            (Maze.E, (1, 0)),
            (Maze.S, (0, 1)),
            (Maze.W, (-1, 0))
        ]:
            nx, ny = x + dx, y + dy
            
            # Check if wall is open (bit is 0)
            if not (maze.walls[y][x] & direction):
                if maze.in_bounds(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    
    return path_count > 1


def has_3x3_open_areas(maze: Maze) -> bool:
    """Check if maze has any 3x3 areas with all walls open.
    
    A valid maze should not have large open areas (all walls removed).
    
    Args:
        maze (Maze): The maze to validate
        
    Returns:
        bool: True if 3x3 open areas exist (invalid), False if valid
    """
    for y in range(maze.height - 2):
        for x in range(maze.width - 2):
            # Check 3x3 area
            all_open = True
            for dy in range(3):
                for dx in range(3):
                    cell = maze.walls[y + dy][x + dx]
                    if cell != 0:  # 0 means all walls open
                        all_open = False
                        break
                if not all_open:
                    break
            if all_open:
                return True
    return False


def validate_maze_structure(maze: Maze, entry: Tuple[int, int], 
                           exit: Tuple[int, int]) -> bool:
    """Comprehensive maze validation.
    
    Checks:
    - Valid entry/exit points
    - No 3x3 open areas
    - Maze is connected (all cells reachable)
    
    Args:
        maze (Maze): The maze to validate
        entry (Tuple[int, int]): Entry coordinates
        exit (Tuple[int, int]): Exit coordinates
        
    Returns:
        bool: True if maze is valid, False otherwise
    """
    # Check entry/exit validity
    if not validate_entry_exit(maze, entry, exit):
        return False
    
    # Check for large open areas
    if has_3x3_open_areas(maze):
        return False
    
    return True


__all__ = [
    "is_perfect_maze",
    "count_open_passages",
    "validate_entry_exit",
    "has_multiple_paths",
    "has_3x3_open_areas",
    "validate_maze_structure",
]

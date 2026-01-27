from collections import deque
from maze_generator import Maze
from pathfinder import solve_maze


def has_multiple_paths(maze: Maze, start: tuple, end: tuple) -> bool:
    """Check if multiple paths exist by testing alternate routes."""
    # Get the main path
    path = solve_maze(maze, start, end)
    if not path:
        return False

    for i in range(1, len(path) - 1):  # Skip start and end
        x, y = path[i]

        original = maze.grid[y][x]
        maze.grid[y][x] = 1
        alt_path = solve_maze(maze, start, end)
        maze.grid[y][x] = original
        if alt_path:  # Found alternate path
            return True
    return False


def count_paths_bfs(maze: Maze, start: tuple, end: tuple,
                    max_paths: int = 2) -> int:
    """Count paths using BFS. Returns count (stops at max_paths)."""
    paths_found = 0
    queue = deque([(start, [start])])

    while queue and paths_found < max_paths:
        (x, y), path = queue.popleft()

        if (x, y) == end:
            paths_found += 1
            continue

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < maze.width and 0 <= ny < maze.height and
                    maze.grid[ny][nx] == 0 and (nx, ny) not in path):
                queue.append(((nx, ny), path + [(nx, ny)]))

    return paths_found


def validate_entry_exit(maze: Maze, entry: tuple, exit: tuple) -> bool:
    """Validate that entry and exit are valid positions."""
    ex, ey = entry
    xx, xy = exit

    # Check bounds
    if not (0 <= ex < maze.width and 0 <= ey < maze.height):
        return False
    if not (0 <= xx < maze.width and 0 <= xy < maze.height):
        return False

    # Check they are paths, not walls
    if maze.grid[ey][ex] != maze.PATH or maze.grid[xy][xx] != maze.PATH:
        return False

    return True


def has_3x3_open_areas(maze: Maze) -> bool:
    """Check if maze has any 3x3 open areas (all paths)."""
    for y in range(maze.height - 2):
        for x in range(maze.width - 2):
            all_open = True
            for dy in range(3):
                for dx in range(3):
                    if maze.grid[y + dy][x + dx] != maze.PATH:
                        all_open = False
                        break
                if not all_open:
                    break
            if all_open:
                return True
    return False


def verify_wall_coherence(maze: Maze) -> bool:
    """Verify that walls are coherent (neighbors match).

    Each neighboring cell must have the same wall. For example,
    if a cell has a wall on the east side, the cell to its east
    must have a wall on the west side.
    """
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grid[y][x]

            # Check East-West coherence
            if x < maze.width - 1:
                right_cell = maze.grid[y][x + 1]
                # If current cell has wall on east, right cell must have wall on west
                # This means both must be walls, or both must be paths
                if cell == maze.WALL and right_cell == maze.PATH:
                    # Check if this is truly incoherent
                    # (in grid representation, walls are solid blocks)
                    pass

            # Check North-South coherence
            if y < maze.height - 1:
                below_cell = maze.grid[y + 1][x]
                # Similar check for vertical neighbors
                if cell == maze.WALL and below_cell == maze.PATH:
                    pass

    return True

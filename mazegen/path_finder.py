from .maze_generator import Maze
from typing import List, Tuple, Optional
import heapq


def astar_find_path(
        maze: Maze, start: Tuple[int, int],
        end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """Find shortest path using A* algorithm (fastest & optimal).

    A* uses Manhattan distance heuristic to guide search,
    making it faster than BFS while guaranteeing shortest path.

    Args:
        maze: Maze object with wall bit-flags
        start: Start coordinates (x, y)
        end: End coordinates (x, y)

    Returns:
        List of (x, y) tuples representing shortest path, or None
    """
    # Validate bounds
    if not (maze.in_bounds(start[0], start[1]) and
            maze.in_bounds(end[0], end[1])):
        return None

    if start == end:
        return [start]

    # Direction mappings for wall checking
    wall_map = {
        (0, -1): (Maze.N, Maze.S),  # North
        (1, 0): (Maze.E, Maze.W),   # East
        (0, 1): (Maze.S, Maze.N),   # South
        (-1, 0): (Maze.W, Maze.E)   # West
    }

    def heuristic(pos: Tuple[int, int]) -> int:
        """Manhattan distance heuristic."""
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

    # A* setup: priority queue with (f_score, counter, position)
    counter = 0
    heap = [(heuristic(start), counter, start)]
    counter += 1

    visited = set()
    parent = {start: None}
    g_score = {start: 0}  # Cost from start to current

    while heap:
        _, _, current = heapq.heappop(heap)

        if current in visited:
            continue

        visited.add(current)

        # Found goal
        if current == end:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        x, y = current
        current_g = g_score[current]

        # Check all 4 neighbors
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)

            # Skip if out of bounds or visited
            if not maze.in_bounds(nx, ny) or neighbor in visited:
                continue

            # Check if wall is open between cells
            wall_from, wall_to = wall_map[(dx, dy)]
            if (not (maze.walls[y][x] & wall_from) and
                    not (maze.walls[ny][nx] & wall_to)):

                tentative_g = current_g + 1

                # Update if we found a better path
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor)
                    parent[neighbor] = current
                    heapq.heappush(heap, (f_score, counter, neighbor))
                    counter += 1

    return None


# Alias for backwards compatibility
def bfs_find_path(
        maze: Maze, start: Tuple[int, int],
        end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """Alias to A* - fastest pathfinding algorithm."""
    return astar_find_path(maze, start, end)


def path_to_moves(path: List[Tuple[int, int]]) -> str:
    """Convert path coordinates to direction string (N/E/S/W).

    Args:
        path: List of (x, y) coordinates

    Returns:
        String of movement letters like "EESSWWN"
    """
    if len(path) < 2:
        return ""

    moves = []
    direction_map = {(0, -1): "N", (1, 0): "E", (0, 1): "S", (-1, 0): "W"}

    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        dx, dy = x2 - x1, y2 - y1
        if (dx, dy) in direction_map:
            moves.append(direction_map[(dx, dy)])

    return "".join(moves)

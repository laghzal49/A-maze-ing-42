from typing import Optional


def solve_maze(maze, start: tuple, end: tuple) -> Optional[list]:
    queue = [start]
    visited = {start}
    parent_map: dict[tuple, Optional[tuple]] = {start: None}

    while queue:
        curr = queue.pop(0)
        if curr == end:
            path = []
            current: Optional[tuple] = curr
            while current is not None:
                path.append(current)
                current = parent_map[current]
            return path[::-1]

        x, y = curr
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if ((0 <= nx < maze.width) and (0 <= ny < maze.height
                                            ) and (
                                                maze.grid[ny][nx] == 0) and (
                                                    (nx, ny) not in visited)):
                visited.add((nx, ny))
                parent_map[(nx, ny)] = curr
                queue.append((nx, ny))
    return None

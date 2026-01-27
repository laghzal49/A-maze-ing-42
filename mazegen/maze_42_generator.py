from typing import Optional
from mazegen.maze_generator import Maze
from mazegen.maze_validator import has_multiple_paths


def generate_perfect_maze_with_42(w: int, h: int, start_pt: tuple,
                                  end_pt: tuple, perfect: bool,
                                  seed: Optional[int]) -> Maze:
    """Generate maze with 42 stamp, ensure single path if perfect=True."""
    max_attempts = 100

    for attempt in range(max_attempts):
        current_seed = seed
        if seed is not None and attempt > 0:
            current_seed = seed + attempt
        elif seed is None:
            current_seed = attempt

        my_maze = Maze(w, h)
        my_maze.generation(1, 1, perfect=perfect, seed=current_seed)

        offset_x, offset_y = (w // 2) - 5, (h // 2) - 3
        forty_two = [(x + offset_x, y + offset_y) for x, y in [
            (2, 1), (2, 2), (2, 3), (4, 1), (4, 2), (4, 3), (4, 4),
            (4, 5), (3, 3), (7, 1), (8, 1), (9, 1), (9, 2), (9, 3),
            (8, 3), (7, 3), (7, 4), (7, 5), (8, 5), (9, 5)
        ]]

        for x in range(offset_x, offset_x + 12):
            for y in range(offset_y, offset_y + 7):
                if 0 <= x < w and 0 <= y < h:
                    my_maze.grid[y][x] = 0
        for x, y in forty_two:
            if 0 <= x < w and 0 <= y < h:
                my_maze.grid[y][x] = 1

        my_maze.grid[start_pt[1]][start_pt[0]] = 0
        my_maze.grid[end_pt[1]][end_pt[0]] = 0

        if perfect:
            if not has_multiple_paths(my_maze, start_pt, end_pt):
                return my_maze
        else:
            return my_maze

    return my_maze

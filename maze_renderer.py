from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from maze_generator import Maze


RESET = "\033[0m"
BOLD = "\033[1m"
BLINK = "\033[5m"
GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
WHITE = "\033[37m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"


def display_terminal(maze: 'Maze', entrance: tuple, exit: tuple,
                     path: Optional[list] = None,
                     highlight_42: bool = False,
                     wall_color: str = 'white') -> None:
    """Render the maze to stdout using ANSI colors.

    - maze: Maze instance with `.grid` 2D list
    - entrance, exit: tuples (x, y)
    - path: list of (x, y) coords to highlight
    - highlight_42: if True, highlight the 42 pattern area
    - wall_color: color for walls ('white', 'cyan', 'green', etc.)
    """
    # Color mapping
    colors = {
        'white': WHITE,
        'cyan': CYAN,
        'green': GREEN,
        'yellow': YELLOW,
        'magenta': MAGENTA,
        'red': RED
    }
    wall_ansi = colors.get(wall_color, WHITE)

    path_set = set(path) if path else set()

    # Calculate 42 pattern area
    w, h = maze.width, maze.height
    offset_x, offset_y = (w // 2) - 5, (h // 2) - 3
    pattern_42 = set()
    if highlight_42:
        for x in range(offset_x, offset_x + 12):
            for y in range(offset_y, offset_y + 7):
                if 0 <= x < w and 0 <= y < h:
                    pattern_42.add((x, y))

    print("\033[H\033[J", end="")

    for y, row in enumerate(maze.grid):
        for x, cell in enumerate(row):
            if (x, y) == entrance:
                print(BOLD + GREEN + " S" + RESET, end="")
            elif (x, y) == exit:
                print(BOLD + RED + " E" + RESET, end="")
            elif (x, y) in path_set:
                print(RED + "██" + RESET, end="")
            elif highlight_42 and (x, y) in pattern_42:
                if cell == 1:
                    print(YELLOW + "██" + RESET, end="")
                else:
                    print(CYAN + "  " + RESET, end="")
            elif cell == 1:
                print(wall_ansi + "██" + RESET, end="")
            else:
                print("  ", end="")
        print()

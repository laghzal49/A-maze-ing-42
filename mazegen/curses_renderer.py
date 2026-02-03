import curses
import random
from typing import List, Optional, Set, Tuple

from .maze_generator import Maze
from .path_finder import bfs_find_path
from .position_selector import get_user_position
from .output_writer import write_output_file

LineParts = List[Tuple[str, int]]


def _draw_maze_line(
    stdscr: "curses.window",
    row: int,
    line_parts: LineParts,
    max_x: int,
) -> None:
    """Draw a single line of the maze."""
    col = 0
    try:
        for text, color in line_parts:
            if col + len(text) >= max_x:
                break
            stdscr.addstr(row, col, text, color)
            col += len(text)
    except curses.error:
        pass


def _build_cell_line(
    maze: Maze,
    y: int,
    player_pos: List[int],
    end: Tuple[int, int],
    path_set: Set[Tuple[int, int]],
    show_path: bool,
    color_42: int,
    color_wall: int,
) -> LineParts:
    """Build the cell content line for a row."""
    line_parts: LineParts = []
    line_parts.append(("|", curses.color_pair(color_wall)))

    for x in range(maze.width):
        cell = maze.walls[y][x]

        if [x, y] == player_pos:
            line_parts.append((" @ ", curses.color_pair(2)))
        elif (x, y) == end:
            line_parts.append((" E ", curses.color_pair(5)))
        elif show_path and (x, y) in path_set:
            line_parts.append((" . ", curses.color_pair(1)))
        elif maze.is_blocked(x, y):
            line_parts.append(("███", curses.color_pair(color_42)))
        else:
            line_parts.append(("   ", curses.color_pair(color_wall)))

        if maze.is_blocked(x, y):
            line_parts.append(("█", curses.color_pair(color_42)))
        else:
            wall = "|" if (cell & maze.E) else " "
            line_parts.append((wall, curses.color_pair(color_wall)))

    return line_parts


def _build_wall_line(
    maze: Maze,
    y: int,
    color_42: int,
    color_wall: int,
) -> LineParts:
    """Build the south wall line for a row."""
    line_parts: LineParts = []
    line_parts.append(("+", curses.color_pair(color_wall)))

    for x in range(maze.width):
        cell = maze.walls[y][x]
        if maze.is_blocked(x, y):
            line_parts.append(("███+", curses.color_pair(color_42)))
        else:
            wall = "---+" if (cell & maze.S) else "   +"
            line_parts.append((wall, curses.color_pair(color_wall)))

    return line_parts


def _initialize_colors() -> None:
    """Initialize curses color pairs."""
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)


def _handle_movement(
    key: int,
    maze: Maze,
    player_pos: List[int],
) -> None:
    """Handle player movement keys."""
    if key in [curses.KEY_UP, ord('w'), ord('W')]:
        new_x, new_y = player_pos[0], player_pos[1] - 1
        if (maze.in_bounds(new_x, new_y) and
                not maze.is_blocked(new_x, new_y)):
            cell = maze.walls[player_pos[1]][player_pos[0]]
            if not (cell & maze.N):
                player_pos[1] = new_y
    elif key in [curses.KEY_DOWN, ord('s'), ord('S')]:
        new_x, new_y = player_pos[0], player_pos[1] + 1
        if (maze.in_bounds(new_x, new_y) and
                not maze.is_blocked(new_x, new_y)):
            cell = maze.walls[player_pos[1]][player_pos[0]]
            if not (cell & maze.S):
                player_pos[1] = new_y
    elif key in [curses.KEY_LEFT, ord('a'), ord('A')]:
        new_x, new_y = player_pos[0] - 1, player_pos[1]
        if (maze.in_bounds(new_x, new_y) and
                not maze.is_blocked(new_x, new_y)):
            cell = maze.walls[player_pos[1]][player_pos[0]]
            if not (cell & maze.W):
                player_pos[0] = new_x
    elif key in [curses.KEY_RIGHT, ord('d'), ord('D')]:
        new_x, new_y = player_pos[0] + 1, player_pos[1]
        if (maze.in_bounds(new_x, new_y) and
                not maze.is_blocked(new_x, new_y)):
            cell = maze.walls[player_pos[1]][player_pos[0]]
            if not (cell & maze.E):
                player_pos[0] = new_x


def setup_phase(
    stdscr: "curses.window",
    maze: Maze,
    config_start: Optional[Tuple[int, int]],
    config_end: Optional[Tuple[int, int]],
) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
    """Setup phase for configuring entry/exit before gameplay."""
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    _initialize_colors()

    start = config_start if config_start else (0, 0)
    end = config_end if config_end else (maze.width - 1, maze.height - 1)

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()

        try:
            stdscr.addstr(0, 0, "MAZE SETUP - Configure Entry and Exit",
                          curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(1, 0, "E=set Entry | X=set Exit | P=Play | Q=Quit")
            stdscr.addstr(2, 0, f"Entry: {start} | Exit: {end}")
            stdscr.addstr(4, 0, "Preview:")
        except curses.error:
            pass

        for y in range(min(maze.height, max_y - 8)):
            line = ""
            for x in range(min(maze.width, max_x - 1)):
                if (x, y) == start:
                    line += "S"
                elif (x, y) == end:
                    line += "E"
                elif maze.is_blocked(x, y):
                    line += "█"
                else:
                    line += "·"
            try:
                stdscr.addstr(5 + y, 0, line)
            except curses.error:
                pass

        stdscr.refresh()
        key = stdscr.getch()

        if key in [ord('q'), ord('Q')]:
            return None, None
        if key in [ord('p'), ord('P')]:
            return start, end
        if key in [ord('e'), ord('E')]:
            start = get_user_position(
                stdscr, maze, "Select START position:", maze.blocked_cells
            )
        if key in [ord('x'), ord('X')]:
            end = get_user_position(
                stdscr, maze, "Select END position:", maze.blocked_cells
            )


def render_maze_curses(
    stdscr: "curses.window",
    maze: Maze,
    path: Optional[List[Tuple[int, int]]] = None,
    start: Optional[Tuple[int, int]] = None,
    end: Optional[Tuple[int, int]] = None,
    algo: str = "dfs",
    seed: Optional[int] = None,
    perfect: bool = True,
    output_file: Optional[str] = None,
) -> None:
    """Render maze using curses with keyboard controls."""
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    _initialize_colors()

    w, h = maze.width, maze.height

    color_42 = 3
    color_wall = 4
    current_algo = algo
    current_perfect = perfect
    current_seed = seed

    status_msg = ""
    start, end = setup_phase(stdscr, maze, start, end)
    if start is None or end is None:
        return

    try:
        path = bfs_find_path(maze, start, end)
        path_set = set(path) if path else set()
        path_found = bool(path)
    except (ValueError, Exception):
        path_set = set()
        path_found = False

    player_pos = list(start)
    show_path = True

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()

        top_line = "+" + "---+" * w
        if len(top_line) < max_x:
            try:
                stdscr.addstr(0, 0, top_line)
            except curses.error:
                pass

        row = 1
        for y in range(h):
            if row >= max_y - 4:
                break

            line1_parts = _build_cell_line(
                maze, y, player_pos, end, path_set,
                show_path, color_42, color_wall
            )
            _draw_maze_line(stdscr, row, line1_parts, max_x)
            row += 1

            if row >= max_y - 4:
                break

            line2_parts = _build_wall_line(maze, y, color_42, color_wall)
            _draw_maze_line(stdscr, row, line2_parts, max_x)
            row += 1

        path_status = "ON" if show_path else "OFF"
        perfect_status = "ON" if current_perfect else "OFF"
        try:
            instructions = [
                f"Arrows/WASD=move | P=path({path_status}) | R=reset | "
                f"N=new pos | A=algo({current_algo}) | "
                f"T=perfect({perfect_status}) | "
                f"G=new seed | S=save | C=42color |"
                f" V=wallcolor | Q=quit",
                f"Pos: ({player_pos[0]}, {player_pos[1]}) | "
                f"Goal: ({end[0]}, {end[1]})"
            ]
            for i, inst in enumerate(instructions):
                if max_y - 2 + i < max_y:
                    stdscr.addstr(max_y - 2 + i, 0, inst)
            if status_msg:
                stdscr.addstr(max_y - 1, 0, status_msg)
        except curses.error:
            pass

        stdscr.refresh()
        key = stdscr.getch()

        if key in [ord('q'), ord('Q')]:
            break
        if key in [ord('p'), ord('P')]:
            show_path = not show_path
        elif key in [ord('r'), ord('R')]:
            maze.generate_maze(
                seed=current_seed, algo=current_algo, perfect=current_perfect
            )
            try:
                path = bfs_find_path(maze, start, end)
                path_set = set(path) if path else set()
                path_found = bool(path)
            except (ValueError, Exception):
                path_set = set()
                path_found = False
            status_msg = "Maze regenerated."
        elif key in [ord('n'), ord('N')]:
            start, end = setup_phase(stdscr, maze, start, end)
            if start is None or end is None:
                break
            player_pos = list(start)
            try:
                path = bfs_find_path(maze, start, end)
                path_set = set(path) if path else set()
                path_found = bool(path)
            except (ValueError, Exception):
                path_set = set()
                path_found = False
            status_msg = "Entry/exit updated."
        elif key in [ord('a'), ord('A')]:
            current_algo = "prim" if current_algo == "dfs" else "dfs"
            maze.generate_maze(
                seed=current_seed, algo=current_algo, perfect=current_perfect
            )
            try:
                path = bfs_find_path(maze, start, end)
                path_set = set(path) if path else set()
                path_found = bool(path)
            except (ValueError, Exception):
                path_set = set()
                path_found = False
            status_msg = f"Algorithm set to {current_algo}."
        elif key in [ord('t'), ord('T')]:
            current_perfect = not current_perfect
            maze.generate_maze(
                seed=current_seed, algo=current_algo, perfect=current_perfect
            )
            try:
                path = bfs_find_path(maze, start, end)
                path_set = set(path) if path else set()
                path_found = bool(path)
            except (ValueError, Exception):
                path_set = set()
                path_found = False
            status_msg = f"Perfect mode {'ON' if current_perfect else 'OFF'}."
        elif key in [ord('s'), ord('S')]:
            if output_file is None:
                status_msg = "Error: no output file configured."
            else:
                try:
                    write_output_file(output_file, maze, start, end)
                    status_msg = f"Saved to {output_file}."
                except Exception as e:
                    status_msg = f"Error: {e}"
        elif key in [ord('c'), ord('C')]:
            color_42 = 3 + (color_42 % 5)
        elif key in [ord('v'), ord('V')]:
            color_wall = 4 + ((color_wall - 4 + 1) % 4)
        else:
            _handle_movement(key, maze, player_pos)

        if player_pos == [end[0], end[1]] and path_found:
            show_path = True
        elif key in [ord('g'), ord('G')]:
            new_seed = random.randint(0, 2**31 - 1)
            if current_seed is None:
                current_seed = new_seed
            else:
                while new_seed == current_seed:
                    new_seed = random.randint(0, 2**31 - 1)
                current_seed = new_seed
            maze.generate_maze(
                seed=current_seed, algo=current_algo, perfect=current_perfect
            )
            try:
                path = bfs_find_path(maze, start, end)
                path_set = set(path) if path else set()
                path_found = bool(path)
            except (ValueError, Exception):
                path_set = set()
                path_found = False
            status_msg = f"Seed updated: {current_seed}."

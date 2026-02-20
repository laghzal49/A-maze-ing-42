import curses
import random
import time
from typing import List, Optional, Set, Tuple

from .maze_generator import Maze
from .ascii_renderer import AsciiCorner, _is_wall_between
from .path_finder import bfs_find_path
from .output_writer import write_output_file
from .animate import animate_path
from .utils import safe_addstr as _safe_addstr

LineParts = List[Tuple[str, int]]


def _draw_maze_line(
    stdscr: "curses.window",
    row: int,
    line_parts: LineParts,
    start_col: int,
    max_x: int,
) -> None:
    """Draw a single line of the maze."""
    col = start_col
    for text, color in line_parts:
        if col >= max_x:
            break
        written = _safe_addstr(stdscr, row, col, text, color, max_x)
        if written == 0:
            break
        col += written


def _build_cell_line(
    maze: Maze,
    y: int,
    player_pos: List[int],
    end: Tuple[int, int],
    path_set: Set[Tuple[int, int]],
    show_path: bool,
    color_42: int,
    color_wall: int,
    vert: List[List[bool]],
) -> LineParts:
    """Build the cell content line for a row."""
    line_parts: LineParts = []

    for x in range(maze.width):
        if x == 0:
            wall = "┃" if vert[0][y] else " "
            line_parts.append((wall, curses.color_pair(color_wall)))

        if [x, y] == player_pos:
            line_parts.append((" ⦻ ", curses.color_pair(6)))
        elif (x, y) == end:
            line_parts.append(("[ ]", curses.color_pair(5)))
        elif show_path and (x, y) in path_set:
            line_parts.append((" o ", curses.color_pair(1)))
        elif maze.is_blocked(x, y):
            line_parts.append(("███", curses.color_pair(color_42)))
        else:
            line_parts.append(("   ", curses.color_pair(color_wall)))

        wall = "┃" if vert[x + 1][y] else " "
        line_parts.append((wall, curses.color_pair(color_wall)))

    return line_parts


def _build_wall_line(
    maze: Maze,
    y: int,
    color_42: int,
    color_wall: int,
    horiz: List[List[bool]],
    vert: List[List[bool]],
) -> LineParts:
    """Build the south wall line for a row."""
    line_parts: LineParts = []
    for jx in range(maze.width + 1):
        left = horiz[y][jx - 1] if jx > 0 else False
        right = horiz[y][jx] if jx < maze.width else False
        up = vert[jx][y - 1] if y > 0 else False
        down = vert[jx][y] if y < maze.height else False
        corner = AsciiCorner.get_corner(left, right, up, down)
        line_parts.append((corner, curses.color_pair(color_wall)))
        if jx < maze.width:
            wall = "━━━" if horiz[y][jx] else "   "
            line_parts.append((wall, curses.color_pair(color_wall)))

    return line_parts


def _compute_wall_grids(
    maze: Maze,
) -> Tuple[List[List[bool]], List[List[bool]]]:
    horiz = [[False for _ in range(maze.width)]
             for _ in range(maze.height + 1)]
    vert = [[False for _ in range(maze.height)]
            for _ in range(maze.width + 1)]

    for jy in range(maze.height + 1):
        for x in range(maze.width):
            if jy == 0:
                horiz[jy][x] = _is_wall_between(maze, x, 0, 0, -1)
            elif jy == maze.height:
                horiz[jy][x] = _is_wall_between(
                    maze, x, maze.height - 1, 0, 1)
            else:
                horiz[jy][x] = _is_wall_between(maze, x, jy - 1, 0, 1)

    for jx in range(maze.width + 1):
        for y in range(maze.height):
            if jx == 0:
                vert[jx][y] = _is_wall_between(maze, 0, y, -1, 0)
            elif jx == maze.width:
                vert[jx][y] = _is_wall_between(
                    maze, maze.width - 1, y, 1, 0)
            else:
                vert[jx][y] = _is_wall_between(maze, jx - 1, y, 1, 0)

    return horiz, vert


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
    if key in [curses.KEY_UP]:
        new_x, new_y = player_pos[0], player_pos[1] - 1
        if (maze.in_bounds(new_x, new_y) and
                not maze.is_blocked(new_x, new_y)):
            cell = maze.walls[player_pos[1]][player_pos[0]]
            if not (cell & maze.N):
                player_pos[1] = new_y
    elif key in [curses.KEY_DOWN]:
        new_x, new_y = player_pos[0], player_pos[1] + 1
        if (maze.in_bounds(new_x, new_y) and
                not maze.is_blocked(new_x, new_y)):
            cell = maze.walls[player_pos[1]][player_pos[0]]
            if not (cell & maze.S):
                player_pos[1] = new_y
    elif key in [curses.KEY_LEFT]:
        new_x, new_y = player_pos[0] - 1, player_pos[1]
        if (maze.in_bounds(new_x, new_y) and
                not maze.is_blocked(new_x, new_y)):
            cell = maze.walls[player_pos[1]][player_pos[0]]
            if not (cell & maze.W):
                player_pos[0] = new_x
    elif key in [curses.KEY_RIGHT]:
        new_x, new_y = player_pos[0] + 1, player_pos[1]
        if (maze.in_bounds(new_x, new_y) and
                not maze.is_blocked(new_x, new_y)):
            cell = maze.walls[player_pos[1]][player_pos[0]]
            if not (cell & maze.E):
                player_pos[0] = new_x


def _terminal_big_enough(
    stdscr: "curses.window",
    min_rows: int,
    min_cols: int,
) -> bool:
    """Check if terminal can display the maze UI."""
    max_y, max_x = stdscr.getmaxyx()
    return max_y >= min_rows and max_x >= min_cols


def _show_terminal_too_small(
    stdscr: "curses.window",
    min_rows: int,
    min_cols: int,
) -> None:
    """Show a clear warning when terminal is too small, then exit."""
    max_y, max_x = stdscr.getmaxyx()
    lines = [
        "Terminal too small for maze UI.",
        f"Required: {min_cols}x{min_rows} (cols x rows)",
        f"Current : {max_x}x{max_y}",
        "Resize terminal and run again.",
        "Press any key to exit.",
    ]
    stdscr.clear()
    y = max(0, (max_y - len(lines)) // 2)
    for i, line in enumerate(lines):
        x = max(0, (max_x - len(line)) // 2)
        _safe_addstr(stdscr, y + i, x, line, curses.color_pair(5), max_x)
    stdscr.refresh()
    stdscr.getch()


def loop_color_message(stdscr: "curses.window", message: str) -> None:
    colors = [1, 2, 3, 4, 5, 6, 7]
    max_y, max_x = stdscr.getmaxyx()
    lines = message.splitlines() or [""]
    y = max(0, (max_y - len(lines)) // 2)

    for color in colors:
        stdscr.clear()
        for i, line in enumerate(lines):
            if y + i >= max_y:
                break
            x = max(0, (max_x - len(line)) // 2)
            _safe_addstr(
                stdscr,
                y + i,
                x,
                line,
                curses.color_pair(color),
                max_x,
            )
        try:
            stdscr.refresh()
        except curses.error:
            pass
        time.sleep(0.25)


def setup_phase(
    stdscr: "curses.window",
    config_start: Optional[Tuple[int, int]],
    config_end: Optional[Tuple[int, int]],
) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
    """Setup phase for configuring entry/exit before gameplay."""
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    try:
        curses.mousemask(0)
        curses.mouseinterval(0)
    except curses.error:
        pass
    _initialize_colors()

    loop_color_message(
        stdscr,
        """
░█████╗░░░░░░░███╗░░░███╗░█████╗░███████╗███████╗░░░░░░██╗███╗░░██╗░██████╗░
██╔══██╗░░░░░░████╗░████║██╔══██╗╚════██║██╔════╝░░░░░░██║████╗░██║██╔════╝░
███████║█████╗██╔████╔██║███████║░░███╔═╝█████╗░░█████╗██║██╔██╗██║██║░░██╗░
██╔══██║╚════╝██║╚██╔╝██║██╔══██║██╔══╝░░██╔══╝░░╚════╝██║██║╚████║██║░░╚██╗
██║░░██║░░░░░░██║░╚═╝░██║██║░░██║███████╗███████╗░░░░░░██║██║░╚███║╚██████╔╝
╚═╝░░╚═╝░░░░░░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚══════╝╚══════╝░░░░░░╚═╝╚═╝░░╚══╝░╚═════╝░
""".strip("\n"),
    )
    loop_color_message(
        stdscr,
        """

██████╗░░█████╗░░██╗░░░░░░░██╗███████╗██████╗░███████╗██████╗░  
██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔══██╗██╔════╝██╔══██╗  
██████╔╝██║░░██║░╚██╗████╗██╔╝█████╗░░██████╔╝█████╗░░██║░░██║  
██╔═══╝░██║░░██║░░████╔═████║░██╔══╝░░██╔══██╗██╔══╝░░██║░░██║  
██║░░░░░╚█████╔╝░░╚██╔╝░╚██╔╝░███████╗██║░░██║███████╗██████╔╝  
╚═╝░░░░░░╚════╝░░░░╚═╝░░░╚═╝░░╚══════╝╚═╝░░╚═╝╚══════╝╚═════╝░  

    ██████╗░██╗░░░██╗  ██╗
    ██╔══██╗╚██╗░██╔╝  ╚═╝
    ██████╦╝░╚████╔╝░  ░░░
    ██╔══██╗░░╚██╔╝░░  ░░░
    ██████╦╝░░░██║░░░  ██╗
    ╚═════╝░░░░╚═╝░░░  ╚═╝

███╗░░░███╗███████╗██╗░░░░░░░░░░░░█████╗░░██████╗██╗░░░░░░█████╗░  
████╗░████║██╔════╝██║░░░░░░░░░░░██╔══██╗██╔════╝██║░░░░░██╔══██╗  
██╔████╔██║█████╗░░██║░░░░░█████╗███████║╚█████╗░██║░░░░░███████║  
██║╚██╔╝██║██╔══╝░░██║░░░░░╚════╝██╔══██║░╚═══██╗██║░░░░░██╔══██║  
██║░╚═╝░██║███████╗███████╗░░░░░░██║░░██║██████╔╝███████╗██║░░██║  
╚═╝░░░░░╚═╝╚══════╝╚══════╝░░░░░░╚═╝░░╚═╝╚═════╝░╚══════╝╚═╝░░╚═╝  

████████╗██╗░░░░░░█████╗░░██████╗░██╗░░██╗███████╗░█████╗░██╗░░░░░░░░
╚══██╔══╝██║░░░░░██╔══██╗██╔════╝░██║░░██║╚════██║██╔══██╗██║░░░░░░░░
░░░██║░░░██║░░░░░███████║██║░░██╗░███████║░░███╔═╝███████║██║░░░░░░░░
░░░██║░░░██║░░░░░██╔══██║██║░░╚██╗██╔══██║██╔══╝░░██╔══██║██║░░░░░░░░
░░░██║░░░███████╗██║░░██║╚██████╔╝██║░░██║███████╗██║░░██║███████╗██╗
░░░╚═╝░░░╚══════╝╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚══════╝╚═╝
    """.strip("\n"))
    return config_start, config_end


def render_maze_curses(
    stdscr: "curses.window",
    maze: Maze,
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
    try:
        curses.mousemask(0)
        curses.mouseinterval(0)
    except curses.error:
        pass

    _initialize_colors()

    min_rows = maze.height * 2 + 1
    min_cols = maze.width * 4 + 1
    if not _terminal_big_enough(stdscr, min_rows, min_cols):
        _show_terminal_too_small(stdscr, min_rows, min_cols)
        return

    h = maze.height
    color_42 = 3
    color_wall = 4
    algo_cycle = ["dfs", "prim", "hunt"]
    current_algo = algo if algo in algo_cycle else "dfs"
    current_perfect = perfect
    current_seed = seed

    status_msg = [""]
    start, end = setup_phase(stdscr, start, end)
    if start is None or end is None:
        return

    path_set: Set[Tuple[int, int]] = set()
    path_ref: List[Optional[List[Tuple[int, int]]]] = [None]
    path_found_ref = [False]

    player_pos = list(start)
    prev_player_pos = list(start)
    show_path = True
    gen_frame_skip = 3
    gen_delay = 0.025
    gen_step_count = [0]
    gen_force_clear = [True]
    gen_skip_animation = [False]
    needs_full_redraw = [False]
    horiz, vert = _compute_wall_grids(maze)
    maze_rows = h * 2 + 1
    maze_cols = maze.width * 4 + 1

    def _compute_layout(max_y: int, max_x: int) -> Tuple[int, int, int, int]:
        # Simplified layout: always center the maze horizontally and
        # vertically.
        # The old right-side panel has been removed, so we no longer reserve
        # space for it. Return panel_left beyond screen and panel_width 0
        # so callers remain compatible.
        maze_left = max(0, (max_x - maze_cols) // 2)
        maze_top = max(0, (max_y - maze_rows) // 2)
        panel_left = max_x + 1
        panel_width = 0
        return maze_top, maze_left, panel_left, panel_width

    def _draw_right_panel(
        max_y: int,
        max_x: int,
        panel_left: int,
        panel_width: int,
        display_status: str,
    ) -> None:
        # Compact UI: draw status above and a single-line menu below the maze,
        # left-aligned at the maze left column. This replaces the boxed
        # right-panel with a compact, non-blocking command line.
        try:
            maze_top_calc = max(0, (max_y - maze_rows) // 2)

            status_row = max(0, min(max_y - 2, maze_top_calc + maze_rows))
            menu_row = max(0, max_y - 1)

            status_text = display_status if display_status else "Ready."
            avail_width = max_x - 2
            if avail_width > 0:
                clipped_status = status_text[:avail_width]
                status_x = max(0, (max_x - len(clipped_status)) // 2)
                _safe_addstr(
                    stdscr, status_row, status_x, clipped_status,
                    curses.color_pair(2), max_x
                )
            path_status = "ON" if show_path else "OFF"
            perfect_status = "ON" if current_perfect else "OFF"
            commands = [
                "Arrows:Move",
                f"P:Path({path_status})",
                "R:Reset",
                f"A:Algo({current_algo})",
                f"T:Perfect({perfect_status})",
                "G:Seed",
                "S:Save",
                "C:Wall + 42 Pattern",
                "Q:Quit",
            ]
            menu_line = " | ".join(commands)
            if len(menu_line) > max_x - 2:
                menu_line = menu_line[: max_x - 2]
            menu_x = max(0, (max_x - len(menu_line)) // 2)
            _safe_addstr(
                stdscr, menu_row, menu_x, menu_line, curses.color_pair(4),
                max_x
            )
        except Exception:
            return

    def _update_player_cell(x: int, y: int, is_player: bool) -> None:
        """Update a single cell for player movement."""
        try:
            max_y, max_x = stdscr.getmaxyx()
            maze_top, maze_left, _, _ = _compute_layout(max_y, max_x)
            # Calculate row position in terminal
            row = maze_top + y * 2 + 1  # Account for wall rows
            if row >= max_y:
                return
            # Build the cell content
            color = color_wall
            if is_player:
                content = " ⦻ "
                color = 6
            elif (x, y) == end:
                content = " E "
                color = 5
            elif show_path and (x, y) in path_set:
                content = "   "
                color = 1
            elif maze.is_blocked(x, y):
                content = "██ "
                color = color_42
            else:
                content = "   "
            # Calculate column position (accounting for walls)
            col = maze_left + x * 4 + 1
            _safe_addstr(stdscr, row, col, content, curses.color_pair(color))
            try:
                stdscr.refresh()
            except curses.error:
                pass
        except curses.error:
            pass

    def _render_frame(
        current_path_set: Optional[Set[Tuple[int, int]]] = None,
        override_status: Optional[str] = None,
        full_clear: bool = True,
    ) -> None:
        if full_clear:
            stdscr.erase()
        max_y, max_x = stdscr.getmaxyx()
        maze_top, maze_left, panel_left, \
            panel_width = _compute_layout(max_y, max_x)
        row = maze_top
        path_to_show = (
            current_path_set
            if current_path_set is not None
            else (path_set if show_path else set())
        )
        for jy in range(h + 1):
            if row >= max_y:
                break

            line_wall = _build_wall_line(
                maze, jy, color_42, color_wall, horiz, vert
            )
            _draw_maze_line(stdscr, row, line_wall, maze_left, max_x)
            row += 1

            if jy == h or row >= max_y:
                break

            line_cell = _build_cell_line(
                maze, jy, player_pos, end, path_to_show,
                True if current_path_set is not None else show_path,
                color_42, color_wall, vert
            )
            _draw_maze_line(stdscr, row, line_cell, maze_left, max_x)
            row += 1

        display_status = (
            override_status if override_status is not None else status_msg[0]
        )
        _draw_right_panel(max_y, max_x, panel_left, panel_width,
                          display_status)

        stdscr.refresh()

    def _update_path_state() -> None:
        try:
            new_path = bfs_find_path(maze, start, end)
            path_ref[0] = new_path
            path_set.clear()
            if new_path:
                path_set.update(new_path)
            path_found_ref[0] = bool(new_path)
        except (ValueError, Exception):
            path_ref[0] = None
            path_set.clear()
            path_found_ref[0] = False

    def _generation_step_callback(
        _cx: int, _cy: int, _nx: int, _ny: int
    ) -> None:
        if gen_skip_animation[0]:
            return
        gen_step_count[0] += 1
        if gen_step_count[0] % gen_frame_skip != 0:
            return
        new_horiz, new_vert = _compute_wall_grids(maze)
        horiz[:] = new_horiz
        vert[:] = new_vert
        # Clear once at generation start to remove stale background content,
        # then avoid full clears to keep animation smooth.
        _render_frame(
            override_status="Generating maze... (Press Q to stop)",
            full_clear=gen_force_clear[0],
        )
        gen_force_clear[0] = False
        stdscr.nodelay(True)
        key = stdscr.getch()
        stdscr.nodelay(False)
        if key in (ord("q"), ord("Q")):
            gen_skip_animation[0] = True
            stdscr.timeout(-1)
            return
        time.sleep(gen_delay)

    def _regenerate_maze(status: str) -> None:
        gen_step_count[0] = 0
        gen_force_clear[0] = True
        gen_skip_animation[0] = False
        # Keep path generation strictly after maze generation.
        path_set.clear()
        path_ref[0] = None
        path_found_ref[0] = False
        maze.generate_maze(
            seed=current_seed,
            algo=current_algo,
            perfect=current_perfect
        )
        _update_path_state()
        new_horiz, new_vert = _compute_wall_grids(maze)
        horiz[:] = new_horiz
        vert[:] = new_vert
        player_pos[:] = [start[0], start[1]]
        prev_player_pos[:] = [start[0], start[1]]
        status_msg[0] = status
        needs_full_redraw[0] = True

    def _animate_current_path() -> None:
        if not path_ref[0]:
            return
        saved_path = list(path_ref[0])
        path_set.clear()
        _render_frame(
            current_path_set=set(),
            override_status="Animating path... (press Q to skip)",
        )
        animate_path(
            stdscr,
            saved_path,
            lambda partial: _render_frame(
                current_path_set=partial,
                override_status="Animating path... (press Q to skip)"
            ),
        )
        path_set.update(saved_path)
        needs_full_redraw[0] = True

    # Animate initial generation first, then render solved-path animation.
    _regenerate_maze("Ready to play (Use ARROWS)")

    # Draw the completed maze first before path animation
    if path_ref[0]:
        _animate_current_path()

    needs_full_redraw[0] = True
    while True:
        if needs_full_redraw[0]:
            _render_frame()
            prev_player_pos = list(player_pos)
            needs_full_redraw[0] = False

        win_handled = False
        if player_pos == [end[0], end[1]] and path_found_ref[0]:
            show_path = True
            status_msg[0] = "You won! Press R to play again or Q to quit."
            _render_frame()
            while True:
                key = stdscr.getch()
                if key in [ord('q'), ord('Q')]:
                    return
                if key in [ord('r'), ord('R')]:
                    _regenerate_maze("New Game Started.")
                    _animate_current_path()
                    needs_full_redraw[0] = True
                    win_handled = True
                    break
        if win_handled:
            continue
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            continue
        if key in [ord('q'), ord('Q')]:
            break
        if key in [ord('p'), ord('P')]:
            show_path = not show_path
            status_msg[0] = f"Path display {'ON' if show_path else 'OFF'}."
            needs_full_redraw[0] = True
        elif key in [ord('r'), ord('R')]:
            _regenerate_maze(
                "Maze regenerated. And ready to play (use ARROWS)")
            _animate_current_path()
        elif key in [ord('a'), ord('A')]:
            idx = algo_cycle.index(current_algo)
            current_algo = algo_cycle[(idx + 1) % len(algo_cycle)]
            _regenerate_maze(
                f"Algorithm set to"
                f" {current_algo} and ready to play (use ARROWS).")
        elif key in [ord('t'), ord('T')]:
            current_perfect = not current_perfect
            _regenerate_maze(
                f"Perfect mode {'ON' if current_perfect else 'OFF'}."
            )
        elif key in [ord('s'), ord('S')]:
            if output_file is None:
                status_msg[0] = "Error: no output file configured."
            else:
                try:
                    write_output_file(output_file, maze, start, end)
                    status_msg[0] = f"Saved to {output_file}."
                except Exception as e:
                    status_msg[0] = f"Error: {e}"
            needs_full_redraw[0] = True
        elif key in [ord('c'), ord('C')]:
            # Merge behavior: C cycles both the '42' color and the wall color.
            color_42 = 3 + (color_42 % 5)
            color_wall = 4 + ((color_wall - 4 + 1) % 4)
            status_msg[0] = (
                f"Colors changed (wall pair {color_wall}, 42 pair {color_42})."
            )
            needs_full_redraw[0] = True
        elif key in [ord('g'), ord('G')]:
            new_seed = random.randint(0, 2**31 - 1)
            if current_seed is None:
                current_seed = new_seed
            else:
                while new_seed == current_seed:
                    new_seed = random.randint(0, 2**31 - 1)
                current_seed = new_seed
            _regenerate_maze(f"Seed updated: {current_seed}.")
        elif key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT,
                     curses.KEY_RIGHT]:
            # Clear old player position
            _update_player_cell(prev_player_pos[0], prev_player_pos[1], False)
            # Move player
            _handle_movement(key, maze, player_pos)
            # Draw new player position
            _update_player_cell(player_pos[0], player_pos[1], True)
            prev_player_pos = list(player_pos)
        else:
            # Handle any other movement keys
            _handle_movement(key, maze, player_pos)

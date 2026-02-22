"""Interactive position selection using curses."""

import curses
from typing import Set, Tuple

from .maze_generator import Maze
from .utils import safe_addstr


def get_user_position(
    stdscr: "curses.window",
    maze: Maze,
    prompt: str,
    blocked: Set[Tuple[int, int]],
) -> Tuple[int, int]:
    """Allow user to select a coordinate via the keyboard."""
    pos = [0, 0]
    while maze.is_blocked(*pos):
        pos[0] += 1

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()

        safe_addstr(
            stdscr,
            0,
            0,
            prompt,
            curses.color_pair(2) | curses.A_BOLD,
            max_x,
        )
        safe_addstr(
            stdscr,
            1,
            0,
            "Use Arrows. ENTER to confirm.",
            curses.color_pair(4),
            max_x,
        )

        is_legal = tuple(pos) not in blocked
        color = curses.color_pair(1) if is_legal else curses.color_pair(5)
        status = " [VALID]" if is_legal else " [BLOCKED!]"
        safe_addstr(
            stdscr,
            2,
            0,
            f"Current: {pos}{status}",
            color,
            max_x,
        )

        key = stdscr.getch()
        if key in [10, 13, curses.KEY_ENTER] and is_legal:
            return (pos[0], pos[1])

        if key in [curses.KEY_UP] and pos[1] > 0:
            pos[1] -= 1
        elif key in [curses.KEY_DOWN] and pos[1] < maze.height - 1:
            pos[1] += 1
        elif key in [curses.KEY_LEFT] and pos[0] > 0:
            pos[0] -= 1
        elif key in [curses.KEY_RIGHT] and pos[0] < maze.width - 1:
            pos[0] += 1

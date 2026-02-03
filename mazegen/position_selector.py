"""Interactive position selection using curses."""

import curses
from typing import Set, Tuple

from .maze_generator import Maze


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

        stdscr.addstr(0, 0, prompt, curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(1, 0, "Use WASD/Arrows. ENTER to confirm.",
                      curses.color_pair(4))

        is_legal = tuple(pos) not in blocked
        color = curses.color_pair(1) if is_legal else curses.color_pair(5)
        status = " [VALID]" if is_legal else " [BLOCKED!]"
        stdscr.addstr(2, 0, f"Current: {pos}{status}", color)

        key = stdscr.getch()
        if key in [10, 13, curses.KEY_ENTER] and is_legal:
            return tuple(pos)

        if key in [curses.KEY_UP, ord('w')] and pos[1] > 0:
            pos[1] -= 1
        elif key in [curses.KEY_DOWN, ord('s')] and pos[1] < maze.height - 1:
            pos[1] += 1
        elif key in [curses.KEY_LEFT, ord('a')] and pos[0] > 0:
            pos[0] -= 1
        elif key in [curses.KEY_RIGHT, ord('d')] and pos[0] < maze.width - 1:
            pos[0] += 1

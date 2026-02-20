import curses
from typing import Optional


def safe_addstr(
    stdscr: "curses.window",
    y: int,
    x: int,
    text: str,
    attr: Optional[int] = None,
    max_x: Optional[int] = None,
) -> int:
    """Safely add a string to the screen, clipping to max_x and
    swallowing curses.error. Returns number of characters written.
    """
    try:
        if max_x is not None and x >= max_x:
            return 0
        if max_x is not None and x + len(text) > max_x:
            text = text[: max(0, max_x - x)]
        if attr is None:
            stdscr.addstr(y, x, text)
        else:
            stdscr.addstr(y, x, text, attr)
        return len(text)
    except curses.error:
        return 0

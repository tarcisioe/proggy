"""Console and cursor control."""
from contextlib import contextmanager
from sys import stdin
from termios import tcgetattr, tcsetattr, TCSANOW
from tty import setcbreak
from typing import Optional


from .position import Position
from .ansi import (
    read_ansi_response, device_status_report_escape, set_cursor_position_escape
)


@contextmanager
def cbreak():
    """Set cbreak on TTY and reset after."""
    attr = tcgetattr(stdin)
    setcbreak(stdin, TCSANOW)
    yield
    tcsetattr(stdin, TCSANOW, attr)


def try_get_cursor_position() -> Optional[Position]:
    """Try to get the cursor position.

    Can fail if there was user input during execution.

    Returns:
        On success, the current cursor position, else None.
    """
    with cbreak():
        print(device_status_report_escape, end='', flush=True)
        y, x = read_ansi_response(stdin.buffer)

    try:
        return Position(int(y), int(x))
    except ValueError:
        return None


def get_cursor_position() -> Position:
    """Get the current cursor position in the TTY.

    Returns:
        The current cursor position.
    """
    position = None

    while position is None:
        position = try_get_cursor_position()

    return position


def set_cursor_position(position: Position):
    """Set the cursor to a given position in the TTY.

    Args:
        position: Where to set the cursor.
    """
    print(set_cursor_position_escape(position), end='', flush=True)


@contextmanager
def at_position(position: Position):
    """Set the cursor position to a given position and move it back after.

    Args:
        position: Where to set the cursor.
    """
    old = get_cursor_position()
    set_cursor_position(position)
    yield
    set_cursor_position(old)


def reserve_space(n_lines: int):
    """Reserve n lines in the console and return the position of the first one.

    Leaves the cursor in the line after the reserved lines.

    Args:
        n_lines: How many lines to reserve.
    """
    print('\n' * (n_lines), end='', flush=True)
    return get_cursor_position() - Position(n_lines, 0)

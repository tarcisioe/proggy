"""TTY-rendering enabled progress bar."""
from dataclasses import dataclass, field, InitVar
from typing import Optional

from ..progress import ProgressBar

from .position import Position

from .console import get_cursor_position, at_position


@dataclass
class TTYProgressBar(ProgressBar):
    """Progress bar capable of "drawing" itself to an ANSI-escape enabled TTY.

    Args:
        position: The position where the progress bar should be rendered.
                  If ommitted, uses the current cursor position.
    """
    position: InitVar[Optional[Position]] = None
    _position: Position = field(init=False)

    def __post_init__(self, starting_progress, position):
        super().__post_init__(starting_progress)
        self._position = (
            position if position is not None else get_cursor_position()
        )

    def draw(self):
        """Draw the progress bar to the tty."""
        with at_position(self._position):
            print(self.render(), end='', flush=True)

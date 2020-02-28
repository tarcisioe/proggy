"""TTY-rendering enabled progress bar."""
from dataclasses import dataclass
from typing import Optional

from ..progress import LogicalProgressBar

from .console import at_position
from .position import Position
from .tty_drawable import TTYDrawable


@dataclass
class _TTYProgressBarData(LogicalProgressBar):
    position: Optional[Position] = None


class TTYProgressBar(  # pylint: disable=abstract-method
    _TTYProgressBarData,
    TTYDrawable
):
    """Progress bar capable of "drawing" itself to an ANSI-escape enabled TTY.

    Args:
        position: The position where the progress bar should be rendered.
                  If ommitted, uses the current cursor position.
    """
    _height = 1

    def _draw(self):
        """Draw the progress bar to the tty."""
        with at_position(self.position):
            print(self.render(), end='', flush=True)


__all__ = ['TTYProgressBar']

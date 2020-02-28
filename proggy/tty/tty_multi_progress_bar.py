"""TTY-rendering enabled progress bar."""
from dataclasses import dataclass, field, InitVar
from typing import List, Optional, Tuple

from ..progress import LogicalProgressBar

from .position import Position
from .tty_drawable import TTYDrawable

from .console import at_position


@dataclass
class _TTYMultiProgressBarData:
    """Mypy doesn't like abstract dataclasses yet."""
    position: Optional[Position] = None
    bars: InitVar[Optional[List[LogicalProgressBar]]] = None

    _bars: List[Tuple[Position, LogicalProgressBar]] = field(
        default_factory=lambda: [], init=False
    )
    _started: bool = field(default=False, init=False)

    def __post_init__(self, bars):
        bars = bars if bars is not None else []

        for delta, bar in enumerate(bars):
            self._bars.append(
                (Position(delta, 0), bar)
            )


class TTYMultiProgressBar(  # pylint: disable=abstract-method
    _TTYMultiProgressBarData,
    TTYDrawable
):
    """Progress bar capable of "drawing" itself to an ANSI-escape enabled TTY.

    Args:
        position: The position where the progress bar should be rendered.
                  If ommitted, uses the current cursor position.
    """
    @property
    def _height(self):
        return len(self._bars)

    def _draw(self):
        """Draw the progress bar to the tty."""
        for delta, bar in self._bars:
            with at_position(self.position + delta):
                print(bar.render(), end='', flush=True)


__all__ = ['TTYMultiProgressBar']

"""TTY-rendering enabled progress bar."""
from dataclasses import dataclass, field, InitVar
from typing import List, Optional, Tuple

from ..errors import BarNotStartedError
from ..progress import LogicalProgressBar

from .position import Position

from .console import at_position, get_cursor_position, reserve_space


@dataclass
class TTYProgressBar(LogicalProgressBar):
    """Progress bar capable of "drawing" itself to an ANSI-escape enabled TTY.

    Args:
        position: The position where the progress bar should be rendered.
                  If ommitted, uses the current cursor position.
    """
    position: Optional[Position] = None

    _started: bool = field(default=False, init=False)

    def __enter__(self):
        self._started = True
        if self.position is None:
            self.position = get_cursor_position()
        self.draw()
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        print()
        self._started = False

    def draw(self):
        """Draw the progress bar to the tty."""
        if not self._started:
            raise BarNotStartedError(
                'This progress bar should only be used as a context manager.'
            )

        with at_position(self.position):
            print(self.render(), end='', flush=True)


@dataclass
class TTYMultiProgressBar:
    """Progress bar capable of "drawing" itself to an ANSI-escape enabled TTY.

    Args:
        position: The position where the progress bar should be rendered.
                  If ommitted, uses the current cursor position.
    """
    position: Optional[Position] = None
    bars: InitVar[Optional[List[LogicalProgressBar]]] = None

    _bars: List[Tuple[Position, LogicalProgressBar]] = field(
        default_factory=lambda: [], init=False
    )
    _started: bool = field(default=False, init=False)

    def __enter__(self):
        self._started = True

        if self.position is None:
            self.position = get_cursor_position()

        self.position = reserve_space(
            len(self._bars),
            starting_position=self.position
        )

        self.draw()
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        print()
        self._started = False

    def __post_init__(self, bars):
        bars = bars if bars is not None else []

        for delta, bar in enumerate(bars):
            self._bars.append(
                (Position(delta, 0), bar)
            )

    def draw(self):
        """Draw the progress bar to the tty."""
        if not self._started:
            raise BarNotStartedError(
                'This progress bar should only be used as a context manager.'
            )

        for delta, bar in self._bars:
            with at_position(self.position + delta):
                print(bar.render(), end='', flush=True)

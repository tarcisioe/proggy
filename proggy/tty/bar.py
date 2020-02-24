"""TTY-rendering enabled progress bar."""
from dataclasses import dataclass, field, InitVar
from typing import List, Optional, Tuple

from ..errors import BarNotStartedError
from ..progress import ProgressBar

from .position import Position

from .console import at_position, get_cursor_position, reserve_space


@dataclass
class TTYProgressBar(ProgressBar):
    """Progress bar capable of "drawing" itself to an ANSI-escape enabled TTY.

    Args:
        position: The position where the progress bar should be rendered.
                  If ommitted, uses the current cursor position.
    """
    position: InitVar[Optional[Position]] = None
    _position: Position = field(init=False)
    _started: bool = field(default=False, init=False)

    def __enter__(self):
        self._started = True
        self.draw()
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        print()
        self._started = False

    def __post_init__(self, starting_progress, position):
        super().__post_init__(starting_progress)
        self._position = (
            position if position is not None else get_cursor_position()
        )

    def draw(self):
        """Draw the progress bar to the tty."""
        if not self._started:
            raise BarNotStartedError(
                'This progress bar should only be used as a context manager.'
            )

        with at_position(self._position):
            print(self.render(), end='', flush=True)


@dataclass
class TTYMultiProgressBar:
    """Progress bar capable of "drawing" itself to an ANSI-escape enabled TTY.

    Args:
        position: The position where the progress bar should be rendered.
                  If ommitted, uses the current cursor position.
    """
    position: InitVar[Optional[Position]] = None
    bars: InitVar[Optional[List[ProgressBar]]] = None
    _bars: List[Tuple[Position, ProgressBar]] = field(
        default_factory=lambda: [], init=False
    )
    _position: Position = field(init=False)
    _started: bool = field(default=False, init=False)

    def __enter__(self):
        self._started = True
        self._position = reserve_space(len(self._bars), starting_position=self._position)
        self.draw()
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        self._started = False

    def __post_init__(self, position, bars):
        self._position = (
            position if position is not None else get_cursor_position()
        )

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
            with at_position(self._position + delta):
                print(bar.render(), end='', flush=True)

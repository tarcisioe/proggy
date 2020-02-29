"""TTY-rendering enabled multi progress bar."""
from __future__ import annotations
from dataclasses import dataclass, field, InitVar
from typing import List, Optional, Tuple

from ..progress import LogicalProgressBar
from ..util import wrapper

from .position import Position
from .tty_drawable import TTYDrawableMixin

from .console import at_position


@dataclass
class _TTYMultiProgressBarData(TTYDrawableMixin['TTYMultiProgressBar']):
    """Mypy crashes if this is part of TTYMultiProgressBar yet."""
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


@dataclass
class MultiProgressBarProxy:
    """Proxy for a multi-progress single bar capable of drawing its parent."""
    bar: LogicalProgressBar
    parent: TTYMultiProgressBar

    size: int = wrapper(lambda self: self.bar)
    total: int = wrapper(lambda self: self.bar)
    characters: str = wrapper(lambda self: self.bar)

    @property
    def progress(self) -> int:
        """Wrap inner bar progress by drawing when it is set."""
        return self.bar.progress

    @progress.setter
    def progress(self, value: int):
        self.bar.progress = value
        self.parent.draw()


class TTYMultiProgressBar(
    _TTYMultiProgressBarData,
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

    def bar_at(self, index: int) -> MultiProgressBarProxy:
        """Get a proxy to the bar at a given index."""
        _, bar = self._bars[index]

        return MultiProgressBarProxy(bar, self)


__all__ = [
    'MultiProgressBarProxy',
    'TTYMultiProgressBar',
]

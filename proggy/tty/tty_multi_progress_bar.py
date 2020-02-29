"""TTY-rendering enabled multi progress bar."""
from __future__ import annotations

from dataclasses import InitVar, dataclass, field
from typing import List, Optional, Tuple

from ..progress import BarInfo, LogicalProgressBar
from .console import at_position
from .drawing_mixin import DrawingWrapperMixin
from .position import Position
from .tty_drawable import TTYDrawableMixin


@dataclass
class _TTYMultiProgressBarData(TTYDrawableMixin['TTYMultiProgressBar']):
    """Mypy crashes if this is part of TTYMultiProgressBar yet."""

    bar_infos: InitVar[Optional[List[BarInfo]]] = None

    _bars: List[Tuple[Position, LogicalProgressBar]] = field(
        default_factory=lambda: [], init=False
    )
    _started: bool = field(default=False, init=False)

    def __post_init__(self, bar_infos) -> None:
        bar_infos = bar_infos if bar_infos is not None else []

        for delta, bar in enumerate(bar_infos):
            self._bars.append((Position(delta, 0), LogicalProgressBar(bar)))


@dataclass
class _MultiProgressBarProxyData:
    bar: LogicalProgressBar
    parent: TTYMultiProgressBar


@dataclass
class MultiProgressBarProxy(DrawingWrapperMixin, _MultiProgressBarProxyData):
    """Proxy for a multi-progress single bar capable of drawing its parent."""

    def draw(self):
        """Draw the parent TTYMultiProgressBar."""
        self.parent.draw()


class TTYMultiProgressBar(_TTYMultiProgressBarData):
    """Progress bar capable of "drawing" itself to an ANSI-escape enabled TTY.

    Args:
        bar_infos: Parameters for initializing the inner progress bars.
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

        return MultiProgressBarProxy(bar=bar, parent=self)


__all__ = [
    'MultiProgressBarProxy',
    'TTYMultiProgressBar',
]

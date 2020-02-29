"""TTY-rendering enabled progress bar."""
from dataclasses import InitVar, dataclass, field

from ..progress import BarInfo, LogicalProgressBar
from .console import at_position
from .drawing_mixin import DrawingWrapperMixin
from .tty_drawable import TTYDrawableMixin


@dataclass
class _TTYProgressBarData:
    bar_info: InitVar[BarInfo]


@dataclass
class TTYProgressBar(
    TTYDrawableMixin['TTYProgressBar'], DrawingWrapperMixin, _TTYProgressBarData,
):
    """Progress bar capable of "drawing" itself to an ANSI-escape enabled TTY.

    Args:
        position: The position where the progress bar should be rendered.
                  If ommitted, uses the current cursor position.
    """

    bar: LogicalProgressBar = field(init=False)
    _height = 1

    def __post_init__(self, bar_info):
        self.bar = LogicalProgressBar(bar_info)

    def _draw(self):
        """Draw the progress bar to the tty."""
        with at_position(self.position):
            print(self.bar.render(), end='', flush=True)


__all__ = ['TTYProgressBar']

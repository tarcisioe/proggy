"""TTY-rendering enabled progress bar."""
from dataclasses import dataclass, InitVar, field
from ..progress import LogicalProgressBar, BarInfo
from ..util import wrapper

from .console import at_position
from .tty_drawable import TTYDrawableMixin


@dataclass
class _TTYProgressBarData:
    bar_info: InitVar[BarInfo]


@dataclass
class TTYProgressBar(
    TTYDrawableMixin['TTYProgressBar'],
    _TTYProgressBarData,
):
    """Progress bar capable of "drawing" itself to an ANSI-escape enabled TTY.

    Args:
        position: The position where the progress bar should be rendered.
                  If ommitted, uses the current cursor position.
    """
    bar: LogicalProgressBar = field(init=False)
    _height = 1

    size: int = wrapper(lambda self: self.bar)
    total: int = wrapper(lambda self: self.bar)
    characters: str = wrapper(lambda self: self.bar)

    @property
    def progress(self) -> int:
        return self.bar.progress

    @progress.setter
    def progress(self, value: int):
        self.bar.progress = value
        self.draw()

    def __post_init__(self, bar_info):
        self.bar = LogicalProgressBar(bar_info)

    def _draw(self):
        """Draw the progress bar to the tty."""
        with at_position(self.position):
            print(self.bar.render(), end='', flush=True)


__all__ = ['TTYProgressBar']

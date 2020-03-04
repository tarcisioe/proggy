"""Mixin for objects that wrap a progress bar and draw a drawable."""
from dataclasses import dataclass
from typing_extensions import Protocol

from ..types import ProgressBar
from ..util import wrapper


class DrawableWithBar(Protocol):
    """A class that has a ProgressBar and can draw itself."""

    bar: ProgressBar

    def draw(self):
        """Draw self somewhere."""
        ...


@dataclass
class DrawingWrapperMixin:
    """Proxy for a multi-progress single bar capable of drawing its parent."""

    size: int = wrapper(lambda self: self.bar)
    total: int = wrapper(lambda self: self.bar)
    characters: str = wrapper(lambda self: self.bar)

    @property
    def progress(self: DrawableWithBar) -> int:
        """Wrap inner bar progress by drawing when it is set."""
        return self.bar.progress

    @progress.setter
    def progress(self: DrawableWithBar, value: int):
        self.bar.progress = value
        self.draw()  # type: ignore

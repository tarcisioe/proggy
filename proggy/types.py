"""Simple vocabulary types and protocols."""
from typing import Protocol, runtime_checkable


@runtime_checkable
class ProgressBar(Protocol):
    """Protocol of every ProgressBar implementation."""
    size: int
    progress: int
    total: int
    characters: str


@runtime_checkable
class Drawable(Protocol):
    """A Drawable object."""
    def draw(self) -> None:
        """Draw the progress bar."""


@runtime_checkable
class DrawableBar(ProgressBar, Drawable, Protocol):
    """Protocol of a drawable bar."""

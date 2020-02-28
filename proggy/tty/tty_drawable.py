"""TTY-drawable base class."""
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from typing import Optional

from .position import Position
from .error import TTYDrawableNotStartedError

from .console import get_cursor_position, reserve_space


@dataclass
class _TTYDrawableData:
    """Mypy doesn't like abstract dataclasses yet."""
    _started: bool = field(default=False, init=False)


class TTYDrawable(ABC, _TTYDrawableData):
    """Abstract TTY-drawable context manager.

    Child classes should provide their own height and method of drawing.
    """
    @abstractproperty
    def position(self) -> Optional[Position]:
        """The object's position."""

    @abstractproperty
    def _height(self) -> int:
        ...

    @abstractmethod
    def _draw(self) -> None:
        """Draw to the TTY."""

    def draw(self) -> None:
        """Draw to the TTY."""
        if not self._started:
            raise TTYDrawableNotStartedError(
                f'{type(self).__name__} objects should only be used as '
                'context managers.'
            )

        self._draw()

    def __enter__(self):
        self._started = True

        if self.position is None:
            self.position = get_cursor_position()

        self.position = reserve_space(
            self._height,
            starting_position=self.position
        )

        self.draw()
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        print()
        self._started = False


__all__ = ['TTYDrawable']

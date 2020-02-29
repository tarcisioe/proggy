"""TTY-drawable base class."""
from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar, cast

from .console import get_cursor_position, reserve_space
from .error import TTYDrawableNotStartedError
from .position import Position

T = TypeVar('T')


@dataclass
class TTYDrawableMixin(Generic[T]):
    """Abstract TTY-drawable context manager.

    Child classes should provide their own height and method of drawing.
    """

    position: Optional[Position] = None
    _started: bool = field(default=False, init=False)
    _height: int = field(init=False)

    def draw(self) -> None:
        """Draw to the TTY."""
        if not self._started:
            raise TTYDrawableNotStartedError(
                f'{type(self).__name__} objects should only be used as '
                'context managers.'
            )

        self._draw()  # type: ignore

    def __enter__(self) -> T:
        self._started = True

        if self.position is None:
            self.position = get_cursor_position()

        self.position = reserve_space(self._height, starting_position=self.position)

        self.draw()
        return cast(T, self)

    def __exit__(self, exc_type, exc, exc_tb):
        print()
        self._started = False


__all__ = ['TTYDrawableMixin']

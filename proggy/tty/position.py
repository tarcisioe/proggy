"""Basic cursor position representation."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    """Represents a position in a text terminal.

    By usual convention for the domain, uses (line, column) notation.
    """

    y: int
    x: int

    def __add__(self, other: Position) -> Position:
        return Position(self.y + other.y, self.x + other.x)

    def __mul__(self, scalar: int) -> Position:
        return Position(self.y * scalar, self.x * scalar)

    def __sub__(self, other: Position) -> Position:
        return self + (other * -1)


__all__ = ['Position']

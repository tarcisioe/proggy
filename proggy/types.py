"""Simple vocabulary types and protocols."""
from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class ProgressBar(Protocol):
    """Protocol of every ProgressBar implementation."""

    size: int
    progress: int
    total: int
    characters: str

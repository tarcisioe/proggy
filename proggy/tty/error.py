"""Error classes for the TTY module."""
from ..error import ProggyError


class TTYDrawableNotStartedError(ProggyError):
    """A drawable type is being outside a with statement."""

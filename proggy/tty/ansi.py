"""All funcionalities related to generating and interpreting ANSI escapes."""
from enum import Enum
from typing import BinaryIO, List, Optional

from .position import Position


class ANSIEscapeType(Enum):
    """Suffixes which define ANSI escape sequence types."""

    CursorPosition = 'H'
    DeviceStatusReport = '6n'


def ansi_escape(kind: ANSIEscapeType, *, values: Optional[List[str]] = None):
    """Generate an ANSI escape string."""
    values = values if values is not None else []

    values_str = ';'.join(values)
    return f'\u001b[{values_str}{kind.value}'


device_status_report_escape = ansi_escape(ANSIEscapeType.DeviceStatusReport)


def set_cursor_position_escape(position: Position):
    """Generate the escape sequence to set the cursor position."""
    return ansi_escape(
        ANSIEscapeType.CursorPosition,
        values=[str(x) for x in [position.y, position.x]],
    )


def read_ansi_response(bytestream: BinaryIO):
    """Read an ANSI response from a bytestream (usually stdin)."""
    buf = bytearray()

    bytestream.read(2)
    while not buf.endswith(b'R'):
        buf += bytestream.read(1)

    return buf[:-1].split(b';')

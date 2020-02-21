"""Main logic behind progress bar rendering."""
from dataclasses import dataclass, field, InitVar

from .errors import ProgressValueError


@dataclass
class _ProgressBarData:
    """Work around dataclasses and properties not being in good speaking terms.

    This makes `dataclass` read the properties and generate the proper method
    without thinking the default value should be the `property` instance.
    """
    size: int
    total: int
    characters: str = ' ⠁⠃⠇⡇⣇⣧⣷⣿'
    starting_progress: InitVar[int] = 0

    _steps: int = field(init=False, repr=False)
    _resolution: int = field(init=False, repr=False)
    _progress: int = field(init=False, repr=False)

    def _steps_and_resolution(self):
        steps = len(self.characters) - 1
        resolution = self.size * (steps)

        return steps, resolution

    def __post_init__(self, starting_progress):
        self._steps, self._resolution = self._steps_and_resolution()
        self._progress = starting_progress


class _ProgressBarValidation(_ProgressBarData):
    """Separate validators from main class logic."""
    @property
    def progress(self) -> int:
        """Get the current progress of the progress bar.

        Returns:
            The current progress (out of self.total).
        """
        return self._progress

    @progress.setter
    def progress(self, value):
        """Set the current progress of the progress bar.

        Raises an error if value is less than zero or over self.total.

        Returns:
            The current progress (out of self.total).
        """
        if self.total < value < 0:
            raise ProgressValueError(
                f'Progress cannot be set higher than {self.total}. '
                f'Value was {value}.'
            )

        self._progress = value


class ProgressBar(_ProgressBarValidation):
    r"""A text-based progress bar.

    The progress bar is composed by three parts, as seen below in between '|':

    |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧                      |
      \    solid    / | \        empty     /
                    leading

    The solid part represents everything in the progress bar that won't change
    anymore.

    The leading character can progress through a sequence of symbols,
    artificially raising the progress bar resolution.

    The empty part is composed of characters that represent progress that
    hasn't yet been reached.

    Args:
        size: The progress bar size in characters.
        total: The total progress capacity of the bar in arbitrary units.
        progress: The starting progress of the progress bar.
        characters: The characters to use for the bar. The first one is the
                    empty one, the last one is the solid one. Everything in
                    between represents the progression of the leading
                    character, from left to right.
    """
    def _filled_amount(self):
        full_ratio = self.progress/self.total

        return int(self._resolution * full_ratio)

    def _solid_size(self, filled):
        return max(0, filled - 1) // self._steps

    def _leading_char_index(self, filled):
        if filled == 0:
            return 0

        return (filled - 1) % self._steps + 1

    def _solid_and_leading(self):
        filled = self._filled_amount()

        solid = self._solid_size(filled) * self.characters[-1]
        leading = self.characters[self._leading_char_index(filled)]

        return solid, leading

    def render(self) -> str:
        """Render the progress bar to a string.

        Returns:
            The rendered progress bar.
        """
        solid, leading = self._solid_and_leading()
        empty = self.characters[0]
        full = f'{solid}{leading}'
        bar = f'{full:{empty}<{self.size}}'

        return bar

"""Main logic behind progress bar rendering."""
from dataclasses import dataclass, field

from .error import ProgressValueError
from .util import checked_property, wrapper


def _positive(name, instance, value: int):
    if value <= 0:
        raise ProgressValueError(
            f'Value for {name} must be positive. Attempted value: {value}.'
        )


def _non_negative(name, instance, value: int):
    if value < 0:
        raise ProgressValueError(
            f'Value for {name} must be non-negative. Attempted value: {value}.'
        )


def _lower_than_total(_, instance, value: int):
    if not 0 <= value <= instance.total:
        raise ProgressValueError(
            f'Value for progress must be between 0 and {instance.total}. '
            f'Attempted value was {value}.'
        )


def _bigger_than_progress(_, instance, value: int):
    try:
        if value < instance.progress:
            raise ProgressValueError(
                f'Value for total cannot lower than current '
                f'progress: {instance.progress}. '
                f'Attempted value was {value}.'
            )
    except KeyError:
        pass


def _more_than_two_characters(_, instance, value: str):
    if len(value) < 2:
        raise ProgressValueError(
            '"characters" must have at least two characters. '
            'At least an empty and a full character must be provided. '
            f'Attempted value: {repr(value)}.'
        )


@dataclass
class BarInfo:
    """Internal progress bar data."""

    size: int = checked_property(validators=(_non_negative,))
    total: int = checked_property(validators=(_non_negative, _bigger_than_progress),)
    progress: int = checked_property(default=0, validators=(_lower_than_total,))
    characters: str = checked_property(
        default=' ⠁⠃⠇⡇⣇⣧⣷⣿', validators=(_more_than_two_characters,)
    )


@dataclass
class LogicalProgressBar:
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
    bar_info: BarInfo
    _steps: int = field(init=False, repr=False)
    _resolution: int = field(init=False, repr=False)

    size: int = wrapper(lambda self: self.bar_info)
    total: int = wrapper(lambda self: self.bar_info)
    progress: int = wrapper(lambda self: self.bar_info)
    characters: str = wrapper(lambda self: self.bar_info)

    def _steps_and_resolution(self):
        steps = len(self.characters) - 1
        resolution = self.size * (steps)

        return steps, resolution

    def __post_init__(self):
        self._steps, self._resolution = self._steps_and_resolution()

    def _filled_amount(self):
        full_ratio = self.progress / self.total

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


__all__ = [
    'BarInfo',
    'LogicalProgressBar',
]

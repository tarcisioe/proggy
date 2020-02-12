from dataclasses import dataclass, field


class ProgressValueError(Exception):
    pass


@dataclass
class ProgressBar:
    """A text-based progress bar.

    The progress bar is composed by three parts, as seen below in between '|':

    |⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧                      |
      \    solid    / | \        empty     /
                    leading

    The solid part represents everything in the progress bar that won't change
    anymore.

    The leading character can progress through a sequence of symbols,
    artificially raising the progress bar resolution.

    The empty part is composed of characters that represent progress that hasn't
    yet been reached.

    Args:
        size: The progress bar size in characters.
        total: The total progress capacity of the bar in arbitrary units.
        characters: The characters to use for the bar. The first one is the
                    empty one, the last one is the solid one. Everything in
                    between represents the progression of the leading character,
                    from left to right.
        progress: The starting progress of the progress bar.
    """
    size: int
    total: int
    characters: str = " ⠁⠃⠇⡇⣇⣧⣷⣿"
    progress: int = 0

    _steps: int = field(init=False)
    _resolution: int = field(init=False)
    # Workaround to have a property. See:
    # https://florimond.dev/blog/articles/2018/10/reconciling-dataclasses-and-properties-in-python/
    _progress: int = field(default=0, init=False, repr=False)

    def __post_init__(self):
        self._steps, self._resolution = self._steps_and_resolution()

    def _steps_and_resolution(self):
        steps = len(self.characters) - 1
        resolution = self.size * (steps)

        return steps, resolution

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

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        if value > self.total:
            raise ProgressValueError(
                f'Progress cannot be set higher than {self.total}. Value was {value}.'
            )

        self._progress = value


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

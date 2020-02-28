from proggy import LogicalProgressBar
from proggy.types import Drawable, DrawableBar, ProgressBar
from proggy.tty import TTYProgressBar, MultiProgressBarProxy, TTYMultiProgressBar


def test() -> None:
    a = LogicalProgressBar(size=30, total=100)
    progress_bar_1: ProgressBar = a
    progress_bar_2: ProgressBar = TTYProgressBar()
    c = TTYMultiProgressBar(bars=[a])
    drawable: Drawable = c
    progress_bar_3: ProgressBar = c.bar_at(0)
    drawable_bar: DrawableBar = c.bar_at(0)

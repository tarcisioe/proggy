from proggy import LogicalProgressBar
from proggy.types import ProgressBar
from proggy.tty import TTYProgressBar, MultiProgressBarProxy, TTYMultiProgressBar


def test() -> None:
    a = LogicalProgressBar(size=30, total=100)
    progress_bar_1: ProgressBar = a
    progress_bar_2: ProgressBar = TTYProgressBar()
    c = TTYMultiProgressBar(bars=[a])
    progress_bar_3: ProgressBar = c.bar_at(0)

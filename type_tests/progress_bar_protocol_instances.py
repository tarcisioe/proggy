from proggy import LogicalProgressBar
from proggy.types import ProgressBar
from proggy.tty import TTYProgressBar


def test() -> None:
    a: ProgressBar = LogicalProgressBar(size=30, total=100)
    b: ProgressBar = TTYProgressBar()
